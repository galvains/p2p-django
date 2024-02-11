import debug_toolbar

from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView

from .views import *
from .authentication import CustomPasswordResetView, CustomPasswordResetConfirmView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('filter/', Filter.as_view(), name='filter'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('activation-info/', ActivationInfo.as_view(), name='activation-info'),

    path('donate/', Donate.as_view(), name='donate'),
    path('successful-payment/', Success.as_view(), name='success'),
    path('failure-payment/', Fail.as_view(), name='fail'),
    path('login/validate_login/', validate_login, name='validate_login'),
    path('register/validate_username/', validate_username, name='validate_username'),
    path('register/validate_email/', validate_email, name='validate_email'),
    path('register/validate_password/', validate_password, name='validate_password'),

    path('activate-user/<uidb64>/<token>', activate_user, name='activate'),

    path('password_reset/', CustomPasswordResetView.as_view(template_name='app/password_reset_form.html',
                                                            email_template_name='app/password_reset_email.html',
                                                            success_url=reverse_lazy('password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
                                                success_url=reverse_lazy('password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
         name='password_reset_complete'),

    path('__debug__/', include(debug_toolbar.urls)),
]
