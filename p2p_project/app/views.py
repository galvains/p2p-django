import os

from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .models import User, TicketsTable
from .utils import generate_token, validator_username, send_activation_email
from .forms import FilterFormAuth, BaseFilterForm, LoginUserForm, RegisterUserForm


class Home(TemplateView):
    template_name = 'app/landing.html'


class Filter(ListView):
    model = TicketsTable
    template_name = 'app/tickets.html'
    object_list = None

    def get_context_data(self, *, object_list=None, **kwargs):

        SEARCH_QUERY = cache.get('SEARCH_QUERY')
        REQUEST_FORM = cache.get('REQUEST_FORM')

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = FilterFormAuth(REQUEST_FORM)
        else:
            context['form'] = BaseFilterForm(REQUEST_FORM)

        context['title'] = 'Tickets'

        if not SEARCH_QUERY and not object_list:
            context['object_list'] = TicketsTable.objects.filter(coin='USDT', currency='USD', trade_type=True,
                                                                 exchange=1).order_by('time_create')
            cache.set(object_list, context['object_list'], 30)

        elif object_list is None:
            if self.request.user.is_authenticated:
                coin = SEARCH_QUERY['coin']
                currency = SEARCH_QUERY['currency']
                trade_type = SEARCH_QUERY['trade_type']
                sort_filter = SEARCH_QUERY['sort']
                exchange = SEARCH_QUERY['exchange']
                if exchange == "all_exchanges":
                    context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                         trade_type=trade_type).order_by(sort_filter)
                else:
                    context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                         trade_type=trade_type,
                                                                         exchange=exchange).order_by(sort_filter)
            else:
                coin = SEARCH_QUERY['coin']
                currency = SEARCH_QUERY['currency']
                trade_type = SEARCH_QUERY['trade_type']
                sort_filter = 'time_create'
                exchange = 1
                context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                     trade_type=trade_type,
                                                                     exchange=exchange).order_by(sort_filter)
        else:
            if self.request.user.is_authenticated:
                coin = object_list['coin']
                currency = object_list['currency']
                trade_type = object_list['trade_type']
                sort_filter = object_list['sort']
                exchange = object_list['exchange']
                if exchange == "all_exchanges":
                    context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                         trade_type=trade_type).order_by(sort_filter)
                else:
                    context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                         trade_type=trade_type,
                                                                         exchange=exchange).order_by(sort_filter)
            else:
                coin = object_list['coin']
                currency = object_list['currency']
                trade_type = object_list['trade_type']
                sort_filter = 'time_create'
                exchange = 1
                context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                     trade_type=trade_type,
                                                                     exchange=exchange).order_by(sort_filter)

        paginator = Paginator(context['object_list'], 25)
        page = self.request.GET.get('page')

        try:
            context['object_list'] = paginator.page(page)
        except PageNotAnInteger:
            context['object_list'] = paginator.page(1)
        except EmptyPage:
            context['object_list'] = paginator.page(paginator.num_pages)
        return context

    def post(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            form = FilterFormAuth(request.POST)
        else:
            form = BaseFilterForm(request.POST)

        if form.is_valid():
            SEARCH_QUERY = form.cleaned_data
            cache.set('SEARCH_QUERY', form.cleaned_data, 30)
            cache.set('REQUEST_FORM', request.POST, 30)
            context = self.get_context_data(object_list=SEARCH_QUERY)
            return render(request, self.template_name, context=context)


class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'app/login.html'

    def get_success_url(self):
        cache.delete('SEARCH_QUERY')
        cache.delete('REQUEST_FORM')
        return reverse_lazy('filter')

    def get_context_data(self, *, object_list=None, **kwargs):
        logout_user(self.request)
        context = super().get_context_data(**kwargs)
        context['data'] = 'Login'
        context['title'] = 'Login'
        return context


class Donate(TemplateView):
    template_name = 'app/donate.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Donate'
        context['CLR_CRYPTO_API'] = os.getenv("CLR_CRYPTO_API")
        context['CLR_SHOP_ID'] = os.getenv("CLR_SHOP_ID")
        return context


class ActivationInfo(TemplateView):
    template_name = 'app/activation_info.html'


class Success(TemplateView):
    template_name = 'app/successful-payment.html'


class Fail(TemplateView):
    template_name = 'app/failure-payment.html'


def register_user(request):
    context = dict()
    context['data'] = 'Register'
    context['title'] = 'Register'

    if request.method == "POST":
        context['form'] = RegisterUserForm(request.POST)
        if context['form'].is_valid():
            cache.delete('SEARCH_QUERY')
            cache.delete('REQUEST_FORM')

            user = context['form'].save(commit=False)
            user.username = context['form'].cleaned_data['username']
            user.email = context['form'].cleaned_data['email']
            user.save()
            user.set_password(context['form'].cleaned_data['password1'])
            user.save()

            send_activation_email(user, request)
            return redirect('activation-info')
    else:
        context['form'] = RegisterUserForm()

    return render(request, 'app/register.html', context=context)


def logout_user(request):
    cache.delete('SEARCH_QUERY')
    cache.delete('REQUEST_FORM')
    auth.logout(request)
    return redirect('filter')


def validate_login(request):
    username = request.GET.get('username', None).lower()
    data = {
        'is_taken_username': User.objects.filter(email=username).exists(),
        'is_taken_email': User.objects.filter(username=username).exists(),
    }
    return JsonResponse(data)


def validate_username(request):
    username = request.GET.get('username', None).lower()
    data = {
        'is_taken': User.objects.filter(username=username).exists(),
        'valid_symbol': validator_username(username),
    }
    return JsonResponse(data)


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email=email).exists(),
    }
    return JsonResponse(data)


def validate_password(request):
    password1 = request.GET.get('password1', None)
    password2 = request.GET.get('password2', None)
    similar = False
    length = False
    digits = True

    if password1 and password2 and password1 == password2:
        similar = True
    if len(password1) >= 8:
        length = True
    if password1.isdigit():
        digits = False

    data = {
        'is_similar': similar,
        'is_length': length,
        'is_digits': digits,
    }

    return JsonResponse(data)


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        return redirect(reverse('login'))
    return render(request, 'activate-failed.html', {'user': user})


def custom_page_not_found_view(request, exception):
    return render(request, "app/error.html", {'type_error': 404})


def custom_error_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 500})


def custom_permission_denied_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 403})


def custom_bad_request_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 400})
