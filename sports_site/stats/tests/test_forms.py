from django.test import TestCase
from league.models import Game, PlayerSeason, SeasonStage, TeamSeason
from stats.models import TeamGameStats, TeamGameLineScore
from stats.forms import (PlayerStatsCreateForm, PlayerPitchingStatsCreateForm,
    LinescoreEditForm, PlayerHittingGameStatsForm, PlayerPitchingGameStatsForm)



class PlayerStatsCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.ts = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1, home_team=cls.ts)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.ts,
            game=cls.game
        )
        # cls.tgs = TeamGameStats.objects.get(season=cls.ts)
        return super().setUpTestData()

    def test_form_labels(self):
        form = PlayerStatsCreateForm(
            **{
                "team_season": self.ts,
                "team_game_stats": self.tgs
            }
        )
        form_labels = {"player": False}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)


    def test_field_qs(self):
        form = PlayerStatsCreateForm(
            **{
                "team_season": self.ts,
                "team_game_stats": self.tgs
            }
        )
        qs = PlayerSeason.objects.filter(team__team=self.ts)
        self.assertQuerysetEqual(qs, form.player_queryset, ordered=False)


    def test_forms(self):
        form_data = {"player": 1}   

        form = PlayerStatsCreateForm(
            data=form_data,
            **{
                "team_season": self.ts,
                "team_game_stats": self.tgs
            }
        )
        self.assertTrue(form.is_valid())



class PlayerPitchingStatsCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.ts = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1, home_team=cls.ts)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.ts,
            game=cls.game
        )
        # cls.tgs = TeamGameStats.objects.get(season=cls.ts)
        return super().setUpTestData()

    def test_form_labels(self):
        form = PlayerPitchingStatsCreateForm(
            **{
                "team_season": self.ts,
                "team_game_stats": self.tgs
            }
        )
        form_labels = {"player": False}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)


    def test_field_qs(self):
        form = PlayerPitchingStatsCreateForm(
            **{
                "team_season": self.ts,
                "team_game_stats": self.tgs
            }
        )
        qs = PlayerSeason.objects.filter(team__team=self.ts)
        self.assertQuerysetEqual(qs, form.player_queryset, ordered=False)


    def test_forms(self):
        form_data = {"player": 1}   

        form = PlayerPitchingStatsCreateForm(
            data=form_data,
            **{
                "team_season": self.ts,
                "team_game_stats": self.tgs
            }
        )
        self.assertTrue(form.is_valid())



class LineScoreEditFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.ts = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1, home_team=cls.ts)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.ts,
            game=cls.game
        )

        cls.tgls = TeamGameLineScore.objects.create(
            game=cls.tgs,
            first=1
        )
        # cls.tgs = TeamGameStats.objects.get(season=cls.ts)
        return super().setUpTestData()


    def test_form_labels(self):
        form = LinescoreEditForm(instance=self.tgls)

        form_labels = {
            "first": "1", "second": "2", "third": "3", "fourth": "4",
            "fifth": "5", "sixth": "6", "seventh": "7", "eighth": "8",
            "ninth": "9", "extras": "Extras"
            }

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        form_data = {"first": 5, "eighth": 3, "extras": "1-0-1"}

        form = LinescoreEditForm(data=form_data, instance=self.tgls)
        self.assertTrue(form.is_valid())


class PlayerHittingGameStatsFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.ts = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1, home_team=cls.ts)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.ts,
            game=cls.game
        )
        return super().setUpTestData()


    def test_form_labels(self):
        form = PlayerHittingGameStatsForm(
            instance=self.tgs,
            **{
                "team_season": self.ts,
                "game_stats": self.tgs
            }
         )

        form_labels = {
            "player": False,
            "batting_order_position": "Order Position",
            "starter": "Starter",
            "substitute": "Sub",
            "at_bats": "AB",
            "plate_appearances": "PA",
            # "hits": "H",
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
            "reached_on_error": "ROE",
            "fielders_choice": "FC",
            "intentional_walks": "IBB", 
            "left_on_base": "LOB",
            "picked_off": "PO",
            "ground_into_double_play": "GIDP",
            "two_out_runs_batted_in": "2-out-RBI"
        }

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)


    def test_forms(self):
        form_data = {
            "player": 1,
            "batting_order_position": 1,
            "starter": True,
            # "substitute": "Sub",
            "at_bats": 4,
            "plate_appearances": 4,
            # "hits": 4,
            "runs": 4,
            "strikeouts" : 0,
            "walks": 0,
            "singles": 0,
            "doubles": 0,
            "triples": 0,
            "homeruns": 4,
            "stolen_bases": 0,
            "caught_stealing": 0,
            "runs_batted_in": 16,
            "hit_by_pitch": 0,
            "sacrifice_flies": 0,
            "sacrifice_bunts": 0,
            "reached_on_error": 0,
            "fielders_choice": 0,
            "intentional_walks": 0, 
            "left_on_base": 0,
            "picked_off": 0,
            "ground_into_double_play": 0,
            "two_out_runs_batted_in": 16
        }

        form = PlayerHittingGameStatsForm(
            data = form_data,
            instance=self.tgs,
            **{
                "team_season": self.ts,
                "game_stats": self.tgs
            }
         )
        self.assertTrue(form.is_valid())



class PlayerPitchingGameStatsFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.stage = SeasonStage.objects.get(id=3)
        cls.ts = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=1, home_team=cls.ts)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.ts,
            game=cls.game
        )
        return super().setUpTestData()


    def test_form_labels(self):
        form = PlayerPitchingGameStatsForm(
            instance=self.tgs,
            **{
                "team_season": self.ts,
                "game_stats": self.tgs
            }
         )

        form_labels = {
            "player": False,
            "win": "W",
            "loss": "L",
            # "game": "G",
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

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)


    def test_forms(self):
        form_data = {
            "player": 1,
            "win": 1,
            "loss": 0,
            # "game": "G",
            "game_started": 1, #Game Starter --> CG --> Booleans or intFields?
            "complete_game": 1, #
            "shutout": 1,
            "save_converted": 0,
            "save_op": 0,
            "hits_allowed": 0,
            "runs_allowed": 0,
            "earned_runs": 0,
            "homeruns_allowed": 0,
            "hit_batters": 0,
            "walks_allowed": 0,
            "strikeouts": 27,
            "stolen_bases_allowed": 0,
            "runners_caught_stealing": 0,
            "pick_offs": 0,
            "balk": 0,
            "innings_pitched": 9,
            "_innings": 0
        }

        form = PlayerHittingGameStatsForm(
            data = form_data,
            instance=self.tgs,
            **{
                "team_season": self.ts,
                "game_stats": self.tgs
            }
         )
        self.assertTrue(form.is_valid())


        