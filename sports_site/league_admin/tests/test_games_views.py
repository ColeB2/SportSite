from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, Season, SeasonStage
from league_admin.forms import EditGameForm

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

    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 1, "game_pk":1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "league_admin/game_templates/game_edit.html")

    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 1, "game_pk":1}))
        self.assertEqual(response.status_code, 200)

        game = Game.objects.get(id=1)
        self.assertEqual(response.context["game_instance"], game)
        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"], "1")
        self.assertTrue(response.context["form"] is not None)
        #More Form Tests context?