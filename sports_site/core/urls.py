from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('<league_url>/', views.find_league, name='league-redirect'),
    path('login/redirect/', views.login_redirect, name='login-redirect'),
    ]