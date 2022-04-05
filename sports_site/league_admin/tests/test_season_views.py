from django.test import TestCase
from django.urls import reverse

from league.models import League, Season, SeasonStage


class LASeasonViewTest(TestCase):
    """
    Tests league_admin_season_view
        from league_admin/views/season_views.py

    'season/',
    views.league_admin_season_view,
    name='league-admin-season')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/')
        self.assertEqual(response.status_code, 302)
        

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_templates/season_page.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league)

        self.assertQuerysetEqual(
            response.context["seasons"], seasons, ordered=False)


class LACreateSeasonViewTest(TestCase):
    """
    Tests league_admin_create_season_view
        from league_admin/views/season_views.py

    'season/add/new',
    views.league_admin_create_season_view,
    name='league-admin-season-create',
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/add/new')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/add/new')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_templates/season_create.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league)

        self.assertQuerysetEqual(
            response.context["seasons"], seasons, ordered=False)
        self.assertTrue(response.context["form"] is not None)

    
    def test_creation(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league)

        data = {"year": 3000}

        response = self.client.post(reverse("league-admin-season-create"),
            data, follow=True)

        self.assertRedirects(response, reverse("league-admin-season"))
