from asyncio import staggered
from django.test import TestCase
from league.models import Game, PlayerSeason, SeasonStage, TeamSeason
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



class TeamGameLineScoreTestCase(TestCase):
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

        cls.tgls = TeamGameLineScore.objects.create(
            game=cls.tgs,
        )
        return super().setUpTestData()

    
    def test_created_properly(self):
        self.assertEqual(self.tgls.first, 0)
        self.assertEqual(self.tgls.second, 0)
        self.assertEqual(self.tgls.third, 0)
        self.assertEqual(self.tgls.fourth, 0)
        self.assertEqual(self.tgls.fifth, 0)
        self.assertEqual(self.tgls.sixth, 0)
        self.assertEqual(self.tgls.seventh, 0)
        self.assertEqual(self.tgls.eighth, 0)
        self.assertEqual(self.tgls.ninth, 0)
        self.assertEqual(self.tgls.extras, "None")

    
    def test_fk_points_properly(self):
        self.assertEqual(self.tgls.game, self.tgs)

    
    def test_labels(self):
        game_label = self.tgls._meta.get_field("game").verbose_name
        first_label = self.tgls._meta.get_field("first").verbose_name
        second_label = self.tgls._meta.get_field("second").verbose_name
        third_label = self.tgls._meta.get_field("third").verbose_name
        fourth_label = self.tgls._meta.get_field("fourth").verbose_name
        fifth_label = self.tgls._meta.get_field("fifth").verbose_name
        sixth_label = self.tgls._meta.get_field("sixth").verbose_name
        seventh_label = self.tgls._meta.get_field("seventh").verbose_name
        eighth_label = self.tgls._meta.get_field("eighth").verbose_name
        ninth_label = self.tgls._meta.get_field("ninth").verbose_name
        extras_label = self.tgls._meta.get_field("extras").verbose_name
        self.assertEqual(game_label, "game")
        self.assertEqual(first_label, "1")
        self.assertEqual(second_label, "2")
        self.assertEqual(third_label, "3")
        self.assertEqual(fourth_label, "4")
        self.assertEqual(fifth_label, "5")
        self.assertEqual(sixth_label, "6")
        self.assertEqual(seventh_label, "7")
        self.assertEqual(eighth_label, "8")
        self.assertEqual(ninth_label, "9")
        self.assertEqual(extras_label, "extras")


    def test_extras_max_length(self):
        max_length = self.tgls._meta.get_field("extras").max_length
        self.assertEqual(max_length, 50)

    
    def test_expected_name(self):
        self.assertEqual(
            str(self.tgls),
            f"{self.tgs.team.team} Linescore for {self.tgs}")


class PlayerHittingGameStatsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1)
        cls.player = PlayerSeason.objects.get(id=1)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game,
        )

        cls.phgs = PlayerHittingGameStats.objects.create(
            team_stats=cls.tgs,
            season=cls.stage,
            player=cls.player
        )

        return super().setUpTestData()


    def test_created_properly(self):
        #Choices
        self.assertEqual(self.phgs.starter, True)
        self.assertEqual(self.phgs.substitute, False)
        #Stats
        stats_defaults_zero = ["batting_order_position",
        "at_bats", "plate_appearances",
        "hits", "runs", "strikeouts", "walks",
        "singles", "doubles", "triples", "homeruns",
        "stolen_bases", "caught_stealing", "runs_batted_in",
        "hit_by_pitch", "sacrifice_flies", "sacrifice_bunts",
        "reached_on_error", "fielders_choice", "intentional_walks", 
        "left_on_base", "picked_off", "ground_into_double_play",
        "two_out_runs_batted_in"
        ]
        for stat_name in stats_defaults_zero:
            stat = self.phgs._meta.get_field(stat_name)
            self.assertEqual(stat.default, 0)

        #Float stats --> Average etc, default None
        self.assertEqual(self.phgs.average, None)
        self.assertEqual(self.phgs.on_base_percentage, None)
        self.assertEqual(self.phgs.slugging_percentage, None)
        self.assertEqual(self.phgs.on_base_plus_slugging, None)


    def test_fk_points_properly(self):
        self.assertEqual(self.phgs.team_stats, self.tgs)
        self.assertEqual(self.phgs.season, self.stage)
        self.assertEqual(self.phgs.player, self.player)

    def test_labels(self):
        phgs_stat_labels = {
            "batting_order_position": "Order Position",
            "starter": "Starter",
            "substitute": "Sub",
            "at_bats": "AB",
            "plate_appearances": "PA",
            "hits": "H",
            "runs": "R",
            "strikeouts" : "SO",
            "walks": "BB",
            "singles": "1B",
            "doubles": "2B",
            "triples": "3B",
            "homeruns": "HR",
            "stolen_bases": "SB",
            "caught_stealing": "CS",
            "runs_batted_in": "RBI",
            "hit_by_pitch": "HBP",
            "sacrifice_flies": "SF",
            "sacrifice_bunts": "SAC",
            "average": "AVG",
            "on_base_percentage": "OBP",
            "slugging_percentage": "SLG",
            "on_base_plus_slugging": "OPS",
            "reached_on_error": "ROE",
            "fielders_choice": "FC",
            "intentional_walks": "IBB", 
            "left_on_base": "LOB",
            "picked_off": "PO",
            "ground_into_double_play": "GIDP",
            "two_out_runs_batted_in": "2-out-RBI"
        }
        for key, val in phgs_stat_labels.items():
            label = self.phgs._meta.get_field(key).verbose_name
            self.assertEqual(label, val)

    def test_expected_name(self):
        self.assertEqual(
            str(self.phgs),
            f"Player: {self.player.player} Game: {self.tgs}"
        )


class PlayerPitchingGameStatsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1)
        cls.player = PlayerSeason.objects.get(id=1)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game,
        )

        cls.ppgs = PlayerPitchingGameStats.objects.create(
            team_stats=cls.tgs,
            season=cls.stage,
            player=cls.player
        )

        return super().setUpTestData()


    def test_created_properly(self):
        #Stats
        stats_defaults_zero = ["win", "loss", "game", "game_started",
            "complete_game", "shutout", "save_converted", "save_op",
            "hits_allowed", "runs_allowed", "earned_runs", "homeruns_allowed",
            "hit_batters", "walks_allowed", "strikeouts", "innings_pitched",
            "_innings", "stolen_bases_allowed", "runners_caught_stealing",
            "pick_offs", "balk"]
        for stat_name in stats_defaults_zero:
            stat = self.ppgs._meta.get_field(stat_name)
            self.assertEqual(stat.default, 0)


    def test_fk_points_properly(self):
        self.assertEqual(self.ppgs.team_stats, self.tgs)
        self.assertEqual(self.ppgs.season, self.stage)
        self.assertEqual(self.ppgs.player, self.player)

    def test_labels(self):
        ppgs_stat_labels = {
            "win": "W",
            "loss": "L",
            "game": "G",
            "game_started": "GS",
            "complete_game": "CG",
            "shutout": "SHO",
            "save_converted": "SV",
            "save_op": "SVO",
            "hits_allowed": "H",
            "runs_allowed": "R",
            "earned_runs": "ER",
            "homeruns_allowed": "HR",
            "hit_batters": "HB",
            "walks_allowed": "BB",
            "strikeouts": "K",
            "stolen_bases_allowed": "SB",
            "runners_caught_stealing": "CS",
            "pick_offs": "PK",
            "balk": "Balk",
            "innings_pitched": "IP",
            "_innings": "IP"
        }
        for key, val in ppgs_stat_labels.items():
            label = self.ppgs._meta.get_field(key).verbose_name
            self.assertEqual(label, val)

    def test_expected_name(self):
        self.assertEqual(
            str(self.ppgs),
            f"Player: {self.player.player} Game: {self.tgs}"
        )
