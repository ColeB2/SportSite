from django.test import TestCase
from django.urls import reverse

from league.models import Season, SeasonStage


class LASeasonStageSelectViewTest(TestCase):
    """
    Tests league_admin_season_stage_select_view
        from league_admin/views/schedule_views.py

    'season/<int:season_year>/<season_pk>',
    views.league_admin_season_stage_select_view,
    name='league-admin-season-stage'),
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": 2022, "season_pk": "1"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": 2022, "season_pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_select_page.html")


    def test_context(self):
        season_year = 2022
        season_pk = 1
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": season_year, "season_pk": season_pk}))
        self.assertEqual(response.status_code, 200)

        season = Season.objects.get(pk=season_pk)
        stages = SeasonStage.objects.filter(season=season)

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season"], season)
        self.assertQuerysetEqual(response.context["stages"], stages, ordered=False)