from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, _unicode_ci_compare
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from django.template import loader

from .models import *

UserModel = get_user_model()


class BaseFilterForm(forms.ModelForm):
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

    coin = forms.ChoiceField(choices=CHOICES_COINS, widget=forms.Select(attrs={'class': 'select'}))
    currency = forms.ChoiceField(choices=CHOICES_CURRENCY, widget=forms.Select(attrs={'class': 'select'}))
    trade_type = forms.ChoiceField(choices=CHOICES_TRADE_TYPE, widget=forms.Select(attrs={'class': 'select'}))

    class Meta:
        model = TicketsTable
        fields = ('coin', 'currency', 'trade_type')


class FilterFormAuth(BaseFilterForm):
    CHOICES_SORT = [
        ('price', 'Low price'),
        ('-price', 'High price'),
        ('time_create', 'Newest'),
        ('-time_create', 'Latest'),
    ]
    CHOICES_EXCHANGES = [
        ('all_exchanges', 'All'),
        (1, 'Binance'),
        (2, 'Bybit'),
        (3, 'Paxful'),
        (4, 'OKX'),
    ]

    exchange = forms.ChoiceField(choices=CHOICES_EXCHANGES, widget=forms.Select(attrs={'class': 'select'}))
    sort = forms.ChoiceField(choices=CHOICES_SORT, widget=forms.Select(attrs={'class': 'select'}))


class FilterFormPaid(FilterFormAuth):
    """
    Filter form for paid users
    """
    pass


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
        self.fields['username'].widget.attrs.update({'placeholder': _('Login')})
        self.fields['password'].widget.attrs.update({'placeholder': _('Password')})

        class Meta:
            model = User
            fields = ('username', 'password')


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': _('Email')}),
    )

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
               and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
            self,
            domain_override=None,
            subject_template_name="registration/password_reset_subject.txt",
            email_template_name="registration/password_reset_email.html",
            use_https=False,
            token_generator=default_token_generator,
            from_email=None,
            request=None,
            html_email_template_name=None,
            extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

class CustomPasswordResetConfirmForm(forms.Form):
    """
    A form that lets a user set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': _('New password')}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': _('Retry new password')}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
