from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, Season, SeasonStage, TeamSeason

###ToDO after implementation
class LAOptionsViewTest(TestCase):
    """
    Tests OptionsView from league_admin/views/options_views.py

    'options/hitting/<int:pk>/edit',
    HittingOptionsUpdateView.as_view(),
    name='league-admin-hitting-options-update'),
    """
    pass
    # def test_view_without_logging_in(self):
    #     response = self.client.get('/league/admin/options/hitting/1/edit')
    #     self.assertEqual(response.status_code, 302)