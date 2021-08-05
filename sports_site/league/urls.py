from django.urls import path
from . import views

urlpatterns = [
    path('player/<int:player_pk>', views.player_page_view, name='player-page'),
    path('team/<int:team_pk>', views.team_page_view, name='team-page'),
    path('team/', views.team_select_page_view, name='team-select-page'),
    path('schedule/', views.schedule_page_view, name="schedule-page"),
    path('game/<int:game_pk>/stats', views.game_boxscore_page_view, name="game-boxscore-page"),
    ]