import os

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, TemplateView, CreateView
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import *
from .utils import *
from .forms import *


class Home(TemplateView):
    template_name = 'app/landing.html'


class Filter(ListView):
    model = TicketsTable
    template_name = 'app/tickets.html'

    context_object_name = 'tickets'
    paginate_by = 15

    def get_queryset(self):
        return TicketsTable.objects.filter(coin='USDT', currency='USD', trade_type=True).order_by('price')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm()
        context['title'] = 'Tickets'
        return context

    def post(self, request, *args, **kwargs):
        form = FilterForm(request.POST)

        if form.is_valid():
            search_query = form.cleaned_data

            coin = search_query['coin']
            currency = search_query['currency']
            trade_type = search_query['trade_type']
            sort_filter = search_query['sort']

            tickets = TicketsTable.objects.filter(coin=coin, currency=currency, trade_type=trade_type).order_by(
                sort_filter)

            page = request.GET.get('page', 1)
            paginator = Paginator(tickets, 15)
            page_object = paginator.page(page)

            context = {
                'form': form,
                'tickets': tickets,
                "page_obj": page_object,
            }

            return render(request, self.template_name, context)


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
