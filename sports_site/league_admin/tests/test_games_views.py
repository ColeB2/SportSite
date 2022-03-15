from django.test import TestCase
from django.urls import reverse


class LADEditGameViewTest(TestCase):
    """
    Tests league_admin_edit_game_view from league_admin/views/game_views.py
    """

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/1/stages/1/1/edit')
        self.assertEqual(response.status_code, 302)