from django.urls import path
from . import views
from .views import (StandingsView, StatsView, PitchingStatsView,
    TeamHittingStatsView, TeamPitchingStatsView)

urlpatterns = [
    path('', StatsView.as_view(), name='stats-page'),
    path('pitching/', PitchingStatsView.as_view(), name='pitching-stats-page'),
    path('team/hitting/', TeamHittingStatsView.as_view(), name='team-stats-page'),
    path('team/pitching/', TeamPitchingStatsView.as_view(), name='team-pitching-stats-page'),
    path('standings/', StandingsView.as_view(), name="standings-page"),
    
    #All Team Stats Info View --> Create,edit delete all objects.
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/info/',
        views.team_game_stats_info_view,
        name='stats-team-game-stats'),

    #Team Game Stats --> Hitting
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/lineup/<int:team_game_stats_pk>/create',
        views.team_game_stats_create_view,
        name='stats-game-stats-create'),
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/lineup/<int:team_game_stats_pk>/edit',
        views.team_game_stats_edit_view,
        name='stats-game-stats-edit'),
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/lineup/<int:team_game_stats_pk>/delete',
        views.team_game_stats_delete_info_view,
        name='stats-game-stats-delete'),
    
    #Team Game Stats --> Pitching
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/pitching/<int:team_game_stats_pk>/create',
        views.team_game_pitching_stats_create_view,
        name='stats-game-pitching-stats-create'),
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/pitching/<int:team_game_stats_pk>/edit',
        views.team_game_pitching_stats_edit_view,
        name='stats-game-pitching-stats-edit'),
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/pitching/<int:team_game_stats_pk>/delete,',
        views.team_game_pitching_stats_delete_info_view,
        name='stats-game-pitching-stats-delete'),
    
    #Team Game Stats --> Linescore
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>',
        views.team_game_linescore_create_view,
        name='stats-linescore-create'),
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>/<int:linescore_pk>/edit',
        views.team_game_linescore_edit_view,
        name='stats-linescore-edit'),
    path(
        'game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>/<int:linescore_pk>/delete',
        views.team_game_linescore_delete_info_view,
        name='stats-linescore-delete'),
    ]