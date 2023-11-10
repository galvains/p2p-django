import os

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

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
        context['form'] = FilterForm(REQUEST_FORM)
        context['title'] = 'Tickets'

        if not SEARCH_QUERY and not object_list:
            context['object_list'] = TicketsTable.objects.filter(coin='USDT', currency='USD', trade_type=True).order_by(
                'price')
            cache.set(object_list, context['object_list'], 30)

        elif object_list is None:
            coin = SEARCH_QUERY['coin']
            currency = SEARCH_QUERY['currency']
            trade_type = SEARCH_QUERY['trade_type']
            sort_filter = SEARCH_QUERY['sort']
            context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                 trade_type=trade_type).order_by(
                sort_filter)
        else:
            coin = object_list['coin']
            currency = object_list['currency']
            trade_type = object_list['trade_type']
            sort_filter = object_list['sort']
            context['object_list'] = TicketsTable.objects.filter(coin=coin, currency=currency,
                                                                 trade_type=trade_type).order_by(
                sort_filter)

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
        form = FilterForm(request.POST)
        if form.is_valid():
            SEARCH_QUERY = form.cleaned_data
            cache.set('SEARCH_QUERY', form.cleaned_data, 30)
            cache.set('REQUEST_FORM', request.POST, 30)

            context = self.get_context_data(object_list=SEARCH_QUERY)
            return render(request, self.template_name, context=context)


"""
class Filter(ListView):
    model = TicketsTable
    template_name = 'app/tickets.html'

    context_object_name = 'tickets'
    paginate_by = 15

    LAST_SEARCH_QUERY = dict()

    def get_queryset(self):
        from_cache_name = 'data'
        from_cache = cache.get(from_cache_name)

        if from_cache:
            data = from_cache
        else:
            data = TicketsTable.objects.filter(coin='USDT', currency='USD', trade_type=True).\
                order_by('price')[:50]
            cache.set(from_cache_name, data, 30)
        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm()
        context['title'] = 'Tickets'
        return context

    def post(self, request, *args, **kwargs):
        form = FilterForm(request.POST)

        from_cache_name = 'data'
        from_cache = cache.get(from_cache_name)

        if form.is_valid():
            search_query = form.cleaned_data

            if self.LAST_SEARCH_QUERY == search_query:
                tickets = from_cache
            else:
                coin = search_query['coin']
                currency = search_query['currency']
                trade_type = search_query['trade_type']
                sort_filter = search_query['sort']
                auto_refresh = search_query['auto_refresh']

                tickets = TicketsTable.objects.filter(coin=coin, currency=currency, trade_type=trade_type).order_by(
                    sort_filter)
                cache.set(from_cache_name, tickets, 30)

                self.LAST_SEARCH_QUERY['coin'] = search_query['coin']
                self.LAST_SEARCH_QUERY['currency'] = search_query['currency']
                self.LAST_SEARCH_QUERY['trade_type'] = search_query['trade_type']
                self.LAST_SEARCH_QUERY['sort'] = search_query['sort']
                self.LAST_SEARCH_QUERY['auto_refresh'] = search_query['auto_refresh']

            page = request.GET.get('page', 1)
            paginator = Paginator(tickets, 15)
            page_object = paginator.page(page)

            context = {
                'form': form,
                'tickets': tickets,
                "page_obj": page_object,
            }

            return render(request, self.template_name, context)

"""


class Register(CreateView):
    form_class = RegisterUserForm
    template_name = 'app/login.html'
    success_url = reverse_lazy('filter')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Register'
        context['title'] = 'Register'
        return context


class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'app/login.html'

    def get_success_url(self):
        return reverse_lazy('filter')

    def get_context_data(self, *, object_list=None, **kwargs):
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
    logout(request)
    return redirect('filter')


def custom_page_not_found_view(request, exception):
    return render(request, "app/error.html", {'type_error': 404})


def custom_error_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 500})


def custom_permission_denied_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 403})


def custom_bad_request_view(request, exception=None):
    return render(request, "app/error.html", {'type_error': 400})
