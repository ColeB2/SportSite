from django.test import TestCase
from django.urls import reverse

from league.models import League, Team


class LAUsersViewTest(TestCase):
    """
    Tests league_admin_users_view
        from league_admin/views/user_views.py

    'users/',
    views.league_admin_users_view,
    name='league-admin-users'),
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/users/')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/users/')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-users"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-users"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/user_templates/users_page.html")

    
    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-users"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        teams = Team.objects.filter(league=league)

        self.assertEqual(response.context["league"], league)
        self.assertQuerysetEqual(response.context["teams"], teams, ordered=False)