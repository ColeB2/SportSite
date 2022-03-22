from django.test import TestCase
from django.urls import reverse


class LAScheduleSelectViewTest(TestCase):
    """
    Tests league_admin_schedule_select_view
        from league_admin/views/schedule_views.py

    'schedule/',
    views.league_admin_schedule_select_view,
    name='league-admin-schedule-select'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/schedule')
        self.assertEqual(response.status_code, 302)