from django.urls import path, include
import debug_toolbar
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('filter/', Filter.as_view(), name='filter'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('donate/', Donate.as_view(), name='donate'),
    path('successful-payment/', Success.as_view(), name='success'),
    path('failure-payment/', Fail.as_view(), name='fail'),
    path('register/validate_username/', validate_username, name='validate_username'),
    path('register/validate_email/', validate_email, name='validate_email'),
    path('__debug__/', include(debug_toolbar.urls)),
]



