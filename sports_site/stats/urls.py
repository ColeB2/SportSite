from django.urls import path
from . import views

urlpatterns = [
    # path('', views.roster_select, name='')
    path('game/<int:game_pk>/team/<int:team_season_pk>/add', views.add_game_stats_view, name='stats-add-game-stats'),
    ]