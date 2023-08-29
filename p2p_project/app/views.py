from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import ListView, View, TemplateView, CreateView, UpdateView, FormView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django_tables2 import RequestConfig, LazyPaginator

from .models import *
from .utils import *
from .forms import *


# def home(request):
#     tickets = TicketsTable.objects.all()
#     tot = tickets.count()

# if not request.method == 'POST':
#     if 'search-persons-post' in request.session:
#         request.POST = request.session['search-persons-post']
#         request.method = 'POST'
#
# if request.method == 'POST':
#     form = FilterForm(request.POST)
#     request.session['search-persons-post'] = request.POST
#     if form.is_valid():
#         coin = form.cleaned_data['coin']
#         currency = form.cleaned_data['currency']
#         trade_type = form.cleaned_data['trade_type']
#
#         tickets = TicketsTable.objects.filter(coin=coin, currency=currency, trade_type=trade_type)
#
#         # page = request.GET.get('page', 1)
#         # paginator = Paginator(tickets, 15)
#         # page_object = paginator.page(page)
# else:
#     form = FilterForm()
#
# table = TicketsTable(tickets)
# RequestConfig(request, paginate={"paginator_class": LazyPaginator}).configure(table)
#
# context = {
#     'table': table,
#     'search_tot': tickets.count(),
#     'form': form,
#     'tot': tot,
# }
#
# return render(request, 'app/tickets.html', context)

class Home(TemplateView):
    template_name = 'app/face.html'


class Filter(ListView):
    model = TicketsTable
    template_name = 'app/tickets.html'

    context_object_name = 'tickets'
    paginate_by = 15

    def get_queryset(self):
        return TicketsTable.objects.filter(coin='USDT', currency='USD', trade_type='BUY').order_by(
            'time_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = FilterForm(request.POST)

        if form.is_valid():
            search_query = form.cleaned_data

            coin = search_query['coin']
            currency = search_query['currency']
            trade_type = search_query['trade_type']

            tickets = TicketsTable.objects.filter(coin=coin, currency=currency, trade_type=trade_type)

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
    template_name = 'app/registration.html'
    success_url = reverse_lazy('filter')


class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'app/login.html'

    def get_success_url(self):
        return reverse_lazy('filter')


def logout_user(request):
    logout(request)
    return redirect('filter')
