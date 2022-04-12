from django.test import TestCase
from django.urls import reverse

from league.models import League, Team


class LATeamSeasonInfoViewTest(TestCase):
    """
    Tests league_admin_team_create_view
        from league_admin/views/team_views.py

    'teams/add',
    views.league_admin_team_create_view,
    name='league-admin-team-create'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/teams/add')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/teams/add')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_templates/team_create.html")

    
    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context["form"] is not None)


    def test_create_team(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        pre_len = Team.objects.filter(league=league).count()
        post = {"name": "Team Name", "place": "Place Name", "abbreviation": "ABR"}

        response = self.client.post(reverse("league-admin-team-create"),
            post,
            follow=True)

        post_len = Team.objects.filter(league=league).count()
        self.assertEqual(pre_len+1, post_len)

    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)
        
        post = {"name": "Team Name", "place": "Place Name", "abbreviation": "ABR"}

        response = self.client.post(reverse("league-admin-team-create"),
            post,
            follow=True)

        self.assertRedirects(response, reverse("league-admin-dashboard"))

        