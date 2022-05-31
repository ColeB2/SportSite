from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from league.models import Game, League, Player, SeasonStage, Team, TeamSeason
from stats.models import PlayerHittingGameStats, TeamGameStats, TeamGameLineScore

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
        self.assertEqual(type(response.context["table"]), PlayerPageHittingStatsTable)
        self.assertEqual(type(response.context["split_table"]), PlayerPageGameHittingStatsSplitsTable)
        self.assertEqual(type(response.context["last_x_table"]), PlayerPageHittingStatsSplitsTable)


class SchedulePageViewTest(TestCase):
    """
    Tests schedule_page_view from league/views.py
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/schedule/?league=TL')
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
        self.assertEqual(team1r, response.context["team_season"][0])


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
        response = self.client.get(reverse('team-select-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)

        self.assertTrue(team in response.context["teams"])
        self.assertTrue(team2 in response.context["teams"])
        self.assertEqual(league, response.context["league"])


class GameBoxscorePageViewTest(TestCase):
    """
    Tests game_boxscore_page_view from league/views.py
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/game/1/stats?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('game-boxscore-page', args="1")+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('game-boxscore-page', args="1")+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league/game_boxscore_page.html')

    def test_tables(self):
        response = self.client.get(reverse('game-boxscore-page', args="1")+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context["home_stats_table"]), PlayerHittingGameStatsTable)
        self.assertEqual(type(response.context["away_stats_table"]), PlayerHittingGameStatsTable)
        self.assertEqual(type(response.context["home_pitching_stats_table"]), PlayerPitchingGameStatsTable)
        self.assertEqual(type(response.context["away_pitching_stats_table"]), PlayerPitchingGameStatsTable)
        self.assertEqual(type(response.context["boxscore_table"]), TeamGameLineScoreTable)
        self.assertEqual(type(response.context["home_boxscore"]), BattingOrderTable)
        self.assertEqual(type(response.context["away_boxscore"]), BattingOrderTable)
        self.assertEqual(type(response.context["home_pitching"]), PitchingOrderTable)
        self.assertEqual(type(response.context["away_pitching"]), PitchingOrderTable)

    def test_context(self):
        league = League.objects.get(id=1)
        team = Team.objects.get(name="Team One")
        team2 = Team.objects.get(name="Team Two")
        gdate = datetime(2020, 5, 18)
        stage = SeasonStage.objects.get(stage=SeasonStage.REGULAR, featured=True)
        team1r = TeamSeason.objects.get(team=team)
        team2r = TeamSeason.objects.get(team=team2)

        game = Game.objects.get(season=stage, home_team=team1r, away_team=team2r, date=gdate)
        hgs = TeamGameStats.objects.get(season=stage, game=game, team=game.home_team)
        hgls = TeamGameLineScore.objects.get(game=hgs)
        # agw = TeamGameStats.objects.get(game=game, team=game.away_team)

        response = self.client.get(reverse('game-boxscore-page', args=str(game.id))+"?league=TL")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(game, response.context["game"])
        self.assertEqual(league, response.context["league"])


        #Need to test, home/away game stats, home/awaystats,
        self.assertEqual(hgs, response.context["home_game_stats"])
        self.assertEqual(hgls, response.context["home_linescore"])
        self.assertQuerysetEqual(hgs.playerhittinggamestats_set.all(), response.context["home_stats"])
        #Currently doesn't get used, or passed.
        ##Currently no stats to test against, test that its a list?
        # print(response.context["home_extra"])
        #homeaway boxscore, homeaway pitching,
        phgs1, phgs2 = PlayerHittingGameStats.objects.all()
        self.assertTrue(phgs1 in response.context["home_stats"])
        self.assertFalse(phgs2 in response.context["home_stats"])
        #home away exxtra, home away linescore


    def test_obj_does_not_exist(self):
        league = League.objects.get(id=1)
        team = Team.objects.get(name="Team One")
        team2 = Team.objects.get(name="Team Two")
        gdate = datetime(2020, 5, 25)
        stage = SeasonStage.objects.get(stage=SeasonStage.REGULAR, featured=True)
        team1r = TeamSeason.objects.get(team=team)
        team2r = TeamSeason.objects.get(team=team2)
        game = Game.objects.create(season=stage, home_team=team1r, away_team=team2r, date=gdate)

        hgs = TeamGameStats.objects.create(season=stage, game=game, team=game.home_team)
        ags = TeamGameStats.objects.create(season=stage, game=game, team=game.away_team)
        
        response = self.client.get(reverse(
            'game-boxscore-page', args=str(game.id))+"?league=TL")
        self.assertEqual(response.status_code, 200)

