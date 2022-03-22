from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, SeasonStage


class LAScheduleSelectViewTest(TestCase):
    """
    Tests league_admin_schedule_select_view
        from league_admin/views/schedule_views.py

    'schedule/',
    views.league_admin_schedule_select_view,
    name='league-admin-schedule-select'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_select.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)

        stages = SeasonStage.objects.filter(
            season__league=League.objects.get(id=1))
        self.assertQuerysetEqual(
            response.context["stages"], stages, ordered=False)



class LAScheduleViewTest(TestCase):
    """
    Tests league_admin_schedule_view
        from league_admin/views/schedule_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>',
    views.league_admin_schedule_view,
    name='league-admin-schedule'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/1')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_view.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=3)
        schedule = Game.objects.filter(season__pk="3")

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"],"3")
        self.assertEqual(response.context["stage"],stage)
        self.assertQuerysetEqual(
            response.context["schedule"],
            schedule,
            ordered=False)