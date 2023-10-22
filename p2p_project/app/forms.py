from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField

from .models import *


class FilterForm(forms.ModelForm):
    CHOICES_COINS = [
        ('USDT', 'USDT'),
        ('BTC', 'BTC'),
        ('ETH', 'ETH'),
        ('USDC', 'USDC'),
    ]
    CHOICES_CURRENCY = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    CHOICES_TRADE_TYPE = [
        (True, 'BUY'),
        (False, 'SELL'),
    ]
    CHOICES_SORT = [
        ('price', 'Low price'),
        ('-price', 'High price'),
        ('time_create', 'Newest'),
        ('-time_create', 'Latest'),
    ]
    CHOISES_REFRESH=[
        (10, '10 sec'),
        (30, '30 sec'),
        (60, '1 min'),
    ]

    coin = forms.ChoiceField(choices=CHOICES_COINS, widget=forms.Select(attrs={'class': 'select'}))
    currency = forms.ChoiceField(choices=CHOICES_CURRENCY, widget=forms.Select(attrs={'class': 'select'}))
    trade_type = forms.ChoiceField(choices=CHOICES_TRADE_TYPE, widget=forms.Select(attrs={'class': 'select'}))
    sort = forms.ChoiceField(choices=CHOICES_SORT, widget=forms.Select(attrs={'class': 'select'}))
    auto_refresh = forms.ChoiceField(choices=CHOISES_REFRESH, widget=forms.Select(attrs={'class': 'select'}))

    class Meta:
        model = TicketsTable
        fields = ('coin', 'currency', 'trade_type')


class RegisterUserForm(UserCreationForm):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': _('Username')})
        self.fields['email'].widget.attrs.update({'placeholder': _('Email')})
        self.fields['password1'].widget.attrs.update({'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Retry password')})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': _('Username')})
        self.fields['password'].widget.attrs.update({'placeholder': _('Password')})

        class Meta:
            model = User
            fields = ('username', 'password')
