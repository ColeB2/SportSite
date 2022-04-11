from django.test import TestCase
from django.urls import reverse

from league.models import League, Season, TeamSeason, SeasonStage


class LATeamSeasonInfoViewTest(TestCase):
    """
    Tests league_admin_team_season_info_view
        from league_admin/views/team_season_views.py

    'season/<int:season_year>/<season_pk>/<season_stage_pk>/<team_name>/<team_season_pk>',
    views.league_admin_team_season_info_view,
    name='league-admin-team-season-info'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/3/TeamOne/1')
        self.assertEqual(response.status_code, 302)