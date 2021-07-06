from django.urls import path
from . import views

urlpatterns = [
    # path('', views.roster_select, name='')
    path('game/<int:game_pk>/team/<int:team_season_pk>/add', views.team_game_stats_edit_view, name='stats-game-stats-edit'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/create', views.team_game_stats_create_view, name='stats-game-stats-create'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/info', views.team_game_stats_info_view, name='stats-team-game-stats'),
    ]