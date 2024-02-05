import os

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.models import User as UserTable

from .models import *
from .utils import *
from .forms import *


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


class Register(CreateView):
    form_class = RegisterUserForm
    template_name = 'app/register.html'

    def get_success_url(self):
        cache.delete('SEARCH_QUERY')
        cache.delete('REQUEST_FORM')
        return reverse('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Register'
        context['title'] = 'Register'
        return context


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


class Success(TemplateView):
    template_name = 'app/successful-payment.html'


class Fail(TemplateView):
    template_name = 'app/failure-payment.html'


def logout_user(request):
    cache.delete('SEARCH_QUERY')
    cache.delete('REQUEST_FORM')
    logout(request)
    return redirect('filter')


def validate_username(request):
    username = request.GET.get('username', None).lower()
    data = {
        'is_taken': UserTable.objects.filter(username=username).exists(),
        'valid_symbol': validator_username(username),
    }
    return JsonResponse(data)


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': UserTable.objects.filter(email=email).exists(),
    }
    return JsonResponse(data)


def custom_page_not_found_view(request, exception):
    return render(request, "app/error.html", {'type_error': 404})


def custom_error_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 500})


def custom_permission_denied_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 403})


def custom_bad_request_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 400})
