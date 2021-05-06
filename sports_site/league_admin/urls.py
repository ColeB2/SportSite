from django.urls import path
from . import views

urlpatterns = [
    path('', views.league_admin_dashboard_view, name='league-admin-dashboard'),
    path('roster/',views.league_admin_roster_select, name='league-admin-roster-select'),
    path('season/',views.league_admin_season_view, name='league-admin-season'),
    path('season/add/new', views.league_admin_create_season_view, name='league-admin-season-create'),
    path('season/<int:season_year>', views.league_admin_season_stage_view, name='league-admin-season-stage'),
    path('season/<int:season_year>/add/new', views.league_admin_create_season_stage_view, name='league-admin-season-stage-create'),
    ]