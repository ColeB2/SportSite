from django.test import TestCase
from django.urls import reverse
from league.models import Game, League, Player, SeasonStage, Team, TeamSeason

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


class SchedulePageViewTest(TestCase):
    """
    Tests schedule_page_view from league/views.py
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/schedule/?league=SBBL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('schedule-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('schedule-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league/schedule_page.html')

    def test_context(self):
        league = League.objects.get(id=1)
        stage = SeasonStage.objects.get(stage=SeasonStage.REGULAR, featured=True)
        games = Game.objects.filter(season=stage)

        response = self.client.get(reverse('schedule-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(league, response.context["league"])
        self.assertEqual(stage, response.context["featured_stage"])

        for game in games:
            self.assertTrue(game in response.context["schedule"])


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


class TeamSelectPageViewTest(TestCase):
    """
    Tests team_select_page_view from league/views.py
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/team/?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('team-select-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('team-select-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league/team_select_page.html')

    def test_context(self):
        league = League.objects.get(id=1)
        team = Team.objects.get(name="Team One")
        team2 = Team.objects.get(name="Team Two")
        response = self.client.get(reverse('team-page', args=str(team.id))+"?league=TL")
        self.assertEqual(response.status_code, 200)

        self.assertTrue(team in response.context["teams"])
        self.assertTrue(team2 in response.context["teams"])
        self.assertEqual(league, response.context["league"])


class GameBoxscorePageViewTest(TestCase):
    """
    Tests game_boxscore_page_view from league/views.py
    """

    # def test_view_url_exists_at_desired_location(self):
    #     response = self.client.get('/league/team/?league=TL')
    #     self.assertEqual(response.status_code, 200)

    # def test_view_accessible_by_name(self):
    #     response = self.client.get(reverse('team-select-page')+"?league=TL")
    #     self.assertEqual(response.status_code, 200)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('team-select-page')+"?league=TL")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'league/team_select_page.html')
    pass
