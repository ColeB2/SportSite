from django.test import TestCase
from league.models import Game, SeasonStage, TeamSeason
from stats.models import (TeamGameStats, TeamGameLineScore,
    PlayerHittingGameStats, PlayerPitchingGameStats)


class TeamGameStatsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game,
        )
        return super().setUpTestData()


    def test_created_properly(self):
        self.assertEqual(self.tgs.runs_for, 0)
        self.assertEqual(self.tgs.runs_against, 0)
        self.assertEqual(self.tgs.win, None)
        self.assertEqual(self.tgs.loss, None)
        self.assertEqual(self.tgs.tie, None)


    def test_fk_point_properly(self):
        self.assertEqual(self.tgs.season, self.stage)
        self.assertEqual(self.tgs.team, self.team_season)
        self.assertEqual(self.tgs.game, self.game)

    
    def test_labels(self):
        season_label = self.tgs._meta.get_field('season').verbose_name
        team_label = self.tgs._meta.get_field('team').verbose_name
        game_label = self.tgs._meta.get_field('game').verbose_name
        runs_for_label = self.tgs._meta.get_field('runs_for').verbose_name
        runs_against_label = self.tgs._meta.get_field('runs_against').verbose_name
        win_label = self.tgs._meta.get_field('win').verbose_name
        loss_label = self.tgs._meta.get_field('loss').verbose_name
        tie_label = self.tgs._meta.get_field('tie').verbose_name
        self.assertEqual(season_label, "season")
        self.assertEqual(team_label, "team")
        self.assertEqual(game_label, "game")
        self.assertEqual(runs_for_label, "runs for")
        self.assertEqual(runs_against_label, "runs against")
        self.assertEqual(win_label, "win")
        self.assertEqual(loss_label, "loss")
        self.assertEqual(tie_label, "tie")


    def test_expected_name(self):
        self.assertEqual(str(self.tgs), f"{self.game} Game Stats")