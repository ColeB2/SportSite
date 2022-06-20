from django.test import TestCase
from django.urls import reverse

from league.models import (Game, League, SeasonStage, TeamSeason)
from stats.filters import HittingSimpleFilter
from stats.models import (PlayerHittingGameStats, 
    TeamGameStats, TeamGameLineScore)
from stats.tables import (ASPlayerHittingGameStatsTable,
    ASPlayerPitchingGameStatsTable, PlayerHittingStatsTable,
    TeamGameLineScoreTable)
from stats.get_stats import get_extra_innings, get_stats



class TeamGameStatsInfoViewTest(TestCase):
    """
    Tests team_game_stats_info_view
    from stats/views/views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/info/',
    views.team_game_stats_info_view,
    name='stats-team-game-stats')
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

    def test_view_without_logging_in(self):
        url = (
            f"/league/stats/" +
            f"game/{self.game.pk}/" +
            f"team/{self.team_season.pk}/info/"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f"/league/stats/" +
            f"game/{self.game.pk}/" +
            f"team/{self.team_season.pk}/info/"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-team-game-stats',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
            }))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-team-game-stats',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "stats/game_stats_info.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-team-game-stats',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game_pk"], self.game.pk)
        self.assertEqual(response.context["team_season_pk"],self.team_season.pk)
        self.assertEqual(response.context["game_stats"], self.tgs)
        player_stats = self.tgs.playerhittinggamestats_set.all()
        self.assertQuerysetEqual(
            response.context["player_stats"], player_stats, ordered=False)
        
        pitching_stats = self.tgs.playerpitchinggamestats_set.all()
        self.assertQuerysetEqual(
            response.context["pitching_stats"], pitching_stats, ordered=False)
        
        #Currently tests table/table2, by recreating table and checking type on
        #the context and the recreated table.
        self.assertEqual(type(response.context["table"]),
            type(ASPlayerHittingGameStatsTable(player_stats)))
        self.assertEqual(type(response.context["table2"]),
            type(ASPlayerPitchingGameStatsTable(pitching_stats)))
    
    def test_linescore_does_not_exist_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-team-game-stats',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["linescore"], None)
        self.assertEqual(response.context["table3"], None)

    def test_linescore_exists_context(self):
        """
        Currently only tests table by recreating table manually and testing
        that the type of the table3 context is equal to type of 
        table we recreate.
        """
        ls = TeamGameLineScore.objects.create(game=self.tgs, ninth=1, extras="1-1")
        td = [get_extra_innings(ls)]
        table = TeamGameLineScoreTable(td)
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-team-game-stats',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
            }))
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.context["linescore"], ls)
        self.assertEqual(type(response.context["table3"]), type(table))
        


class StatsViewTests(TestCase):
    """
    Tests StatsView
    from stats/views/views.py

    '',
    StatsView.as_view(),
    name='stats-page')
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

    def test_view_without_logging_in(self):
        response = self.client.get(f"/league/stats/?league={self.league.url}")
        self.assertEqual(response.status_code, 200)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(f"/league/stats/?league={self.league.url}")
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'stats-page') + f'?league={self.league.url}')
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'stats-page')+f'?league={self.league.url}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stats/stats_page.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'stats-page')+f'?league={self.league.url}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stats/stats_page.html")

        self.assertEqual(response.context["league"], self.league)
        self.assertEqual(response.context["stage"], self.stage)

        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["paginator"].per_page, 25)
        
        table = PlayerHittingStatsTable({})
        self.assertTrue(response.context["table"] is not None)
        self.assertEqual(type(response.context["table"]), type(table))
        
        _filter = HittingSimpleFilter()
        self.assertTrue(response.context["filter"] is not None)
        self.assertEqual(type(response.context["filter"]), type(_filter))

        qs = PlayerHittingGameStats.objects.filter(
            player__player__league=self.league,
            season=self.stage) #queryset --> get hitting_stats
        hs = get_stats(qs, "all_season_hitting") #hitting_stats
        ths = response.context["object_list"]
        self.assertQuerysetEqual(ths, hs, transform=lambda x:x)