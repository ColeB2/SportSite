from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, Season, SeasonStage

class LAEditGameViewTest(TestCase):
    """
    Tests league_admin_edit_game_view from league_admin/views/game_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>/<game_pk>/edit'
    'league-admin-game-edit'
    views.league_admin_edit_game_view
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/1/1/edit')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/1/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 1, "game_pk":1}))
        self.assertEqual(response.status_code, 200)