from django.urls import path
from . import views

urlpatterns = [
    # path('', views.roster_select, name='')
    path('game/<int:game_pk>/team/<int:team_season_pk>/add', views.add_game_stats_view, name='stats-add-game-stats'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/create', views.create_team_game_stats_view, name='stats-create-game-stats'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/<int:team_game_pk>', views.game_stats_info_view, name='stats-team-game-stats'),
    ]