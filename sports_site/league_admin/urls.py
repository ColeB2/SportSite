from django.urls import path
from . import views
from .views import SeasonEditView

urlpatterns = [
    path('', views.league_admin_dashboard_view, name='league-admin-dashboard'),
    path('roster/',views.league_admin_roster_select, name='league-admin-roster-select'),
    path('news/',views.league_admin_news_select, name='league-admin-news-select'),
    path('season/',views.league_admin_season_view, name='league-admin-season'),
    path('season/add/new', views.league_admin_create_season_view, name='league-admin-season-create'),

    path('season/<int:season_year>/<season_pk>', views.league_admin_season_stage_select_view, name='league-admin-season-stage'),
    path('season/<int:season_year>/<season_pk>/<int:pk>/edit', SeasonEditView.as_view(), name='league-admin-season-edit'),
    path('season/<int:season_year>/<season_pk>/delete', views.league_admin_season_delete_info_view, name='league-admin-season-delete'),
    path('season/<int:season_year>/<season_pk>/add/new', views.league_admin_create_season_stage_view, name='league-admin-season-stage-create'),
    path('season/<int:season_year>/<season_pk>/<season_stage_pk>', views.league_admin_season_stage_info_view, name='league-admin-season-stage-info'),
    path('season/<int:season_year>/<season_pk>/<season_stage_pk>/delete', views.league_admin_season_stage_delete_info_view, name='league-admin-season-stage-delete'),

    path('season/<int:season_year>/<season_pk>/<season_stage_pk>/<team_name>/<team_season_pk>',
        views.league_admin_team_season_info_view, name='league-admin-team-season-info'),
    path('season/<int:season_year>/<season_pk>/<season_stage_pk>/<team_name>/<team_season_pk>/delete',
        views.league_admin_team_season_delete_info_view, name='league-admin-team-season-delete'),

    path('players/', views.league_admin_player_select_view, name='league-admin-player-select'),
    path('players/<player_pk>/edit', views.league_admin_player_edit_view, name='league-admin-player-edit'),
    path('players/add', views.league_admin_player_create_view, name='league-admin-player-create'),
    path('players/<player_pk>/delete', views.league_admin_player_delete_info_view, name='league-admin-player-delete'),

    path('schedule/', views.league_admin_schedule_select_view, name='league-admin-schedule-select'),
    path('schedule/<int:season_year>/stages/<season_stage_pk>', views.league_admin_schedule_view, name='league-admin-schedule'),
    path('schedule/<int:season_year>/stages/<season_stage_pk>/edit', views.league_admin_schedule_create_view, name='league-admin-schedule-create'),
    path('schedule/<int:season_year>/stages/<season_stage_pk>/delete', views.league_admin_schedule_delete_info_view, name='league-admin-schedule-delete-info'),
    path('schedule/<int:season_year>/stages/<season_stage_pk>/<game_pk>/edit', views.league_admin_edit_game_view, name='league-admin-game-edit'),
    path('schedule/<int:season_year>/stages/<season_stage_pk>/<game_pk>/delete', views.league_admin_delete_game_info_view, name='league-admin-game-delete'),

    path('users/', views.league_admin_users_view, name='league-admin-users'),
    path('users/<user_name>/<user_pk>', views.league_admin_user_info_view, name='league-admin-user-info'),
    path('users/<user_name>/<user_pk>/edit/permissions/', views.league_admin_user_edit_perms_view, name='league-admin-user-edit-perms'),


    ]