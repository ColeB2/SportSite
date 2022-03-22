from django.test import TestCase
from django.urls import reverse

from league.models import League, SeasonStage


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