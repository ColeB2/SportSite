from django.test import TestCase
from django.urls import reverse
from league.models import League, Player, SeasonStage, Team, TeamSeason

from stats.tables import (BattingOrderTable, PitchingOrderTable,
    PlayerHittingGameStatsTable, PlayerPageGameHittingStatsSplitsTable,
    PlayerPageHittingStatsTable, PlayerPageHittingStatsSplitsTable,
    PlayerPitchingGameStatsTable, TeamGameLineScoreTable)


class PlayerPageViewTest(TestCase):
    """
    Tests player_page_view from league/views.py
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/player/1?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('player-page', args='1')+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('player-page', args='1')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league/player_page.html')

    def test_context(self):
        league = League.objects.get(id=1)
        player = Player.objects.get(league=league, last_name="One")
        player2 = Player.objects.get(league=league, last_name="Two")
        response = self.client.get(reverse('player-page', args=str(player.id))+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(player, response.context["player"])
        self.assertFalse(player2 == response.context["player"])
        self.assertEqual(response.context["table"], type(PlayerPageHittingStatsTable))
        self.assertEqual(response.context["split_table"], type(PlayerPageGameHittingStatsSplitsTable))
        self.assertEqual(response.context["last_x_table"], type(PlayerPageHittingStatsSplitsTable))


class TeamPageViewTest(TestCase):
    """
    Tests team_page_view from league/views.py
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/team/1?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('team-page', args='1')+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('team-page', args='1')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league/team_page.html')

    def test_context(self):
        league = League.objects.get(id=1)
        team = Team.objects.get(name="Team One")
        team2 = Team.objects.get(name="Team Two")
        stage = SeasonStage.objects.get(stage=SeasonStage.REGULAR, featured=True)
        team1r = TeamSeason.objects.get(team=team)

        response = self.client.get(reverse('team-page', args=str(team.id))+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(team, response.context["team"])
        self.assertFalse(team2 == response.context["team"])
        self.assertEqual(league, response.context["league"])
        self.assertEqual(stage, response.context["featured_stage"])
        self.assertEqual(team1r, response.context["team_season"])