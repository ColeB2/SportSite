from django.urls import path
from . import views

urlpatterns = [
    path('', views.stats_display_view, name='stats-page'),
    path('pitching/', views.pitching_stats_display_view, name='pitching-stats-page'),
    path('team/hitting', views.team_stats_display_view, name='team-stats-page'),
    path('standings/', views.standings_display_view, name="standings-page"),
    path('game/<int:game_pk>/team/<int:team_season_pk>/lineup/<int:team_game_stats_pk>/create', views.team_game_stats_create_view, name='stats-game-stats-create'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/pitching/<int:team_game_stats_pk>/create', views.team_game_pitching_stats_create_view, name='stats-game-pitching-stats-create'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/lineup/<int:team_game_stats_pk>/edit', views.team_game_stats_edit_view, name='stats-game-stats-edit'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/pitching/<int:team_game_stats_pk>/edit', views.team_game_pitching_stats_edit_view, name='stats-game-pitching-stats-edit'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/lineup/<int:team_game_stats_pk>/delete,', views.team_game_stats_delete_info_view, name='stats-game-stats-delete'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/pitching/<int:team_game_stats_pk>/delete,', views.team_game_pitching_stats_delete_info_view, name='stats-game-pitching-stats-delete'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/info/', views.team_game_stats_info_view, name='stats-team-game-stats'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>', views.team_game_linescore_create_view, name='stats-linescore-create'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>/<int:linescore_pk>/edit', views.team_game_linescore_edit_view, name='stats-linescore-edit'),
    path('game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>/<int:linescore_pk>/delete', views.team_game_linescore_delete_info_view, name='stats-linescore-delete'),
    ]