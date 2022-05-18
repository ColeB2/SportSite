from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, SeasonStage, TeamSeason
from stats.models import PlayerHittingGameStats, TeamGameStats


class TeamGameStatsCreateViewTest(TestCase):
    """
    Tests team_game_stats_create_view
    from stats/views/tgs_hitting_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/lineup/
        <int:team_game_stats_pk>/create',
    views.team_game_stats_create_view,
    name='stats-game-stats-create'
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