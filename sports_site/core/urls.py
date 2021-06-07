from django.urls import path
from . import views

urlpatterns = [
    # path('', views.roster_select, name='')
    path('', views.landing, name='landing'),
    path('<league_url>/', views.find_league, name='league-redirect'),
    path('login/redirect/', views.login_redirect, name='login-redirect'),
    ]