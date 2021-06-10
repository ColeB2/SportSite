from django.urls import path
from . import views

urlpatterns = [
    # path('', views.roster_select, name='')
    path('', views.landing, name='landing'),
    path('<league_url>/', views.find_league, name='league-redirect'),
    path('game/<int:game_pk>/team/<int:team_pk>/add', views.login_redirect, name='stats-team-game'),
    ]