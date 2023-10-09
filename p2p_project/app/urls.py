from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('filter/', Filter.as_view(), name='filter'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('donate/', Donate.as_view(), name='donate'),
]
