from django.test import TestCase
from django.urls import reverse

from league.models import League
# from league_admin.forms import PlayerCreateForm


class LAPlayerCreateView(TestCase):
    """
    Test league_admin_player_create_view from league_admin/views/player_views.py
    
    'players/add',
    views.league_admin_player_create_view,
    name='league-admin-player-create'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/players/add')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/add')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_create.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        self.assertEqual(response.context["league"], league)
        self.assertTrue(response.context["form"] is not None)