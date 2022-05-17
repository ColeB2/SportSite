from asyncio import staggered
from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, Season, SeasonStage, TeamSeason
from stats.models import TeamGameLineScore, TeamGameStats



class TeamGameLinescoreCreateViewTest(TestCase):
    """
    Tests team_game_linescore_create_view from stats/views/tg_linescore_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/linescore/<int:team_game_stats_pk>',
    views.team_game_linescore_create_view,
    name='stats-linescore-create'

    View does NOT exist as a page
    -->Redirect to stats-team-game-stats
    -->or team_game_stats_info_view
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=1)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

    def test_view_without_logging_in(self):
        response = self.client.get('/league/stats/game/2/team/1/linescore/1')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/stats/game/2/team/1/linescore/1')
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk
            }))
        self.assertEqual(response.status_code, 302)


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk
            }))
        self.assertRedirects(response, reverse("stats-team-game-stats", 
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))
