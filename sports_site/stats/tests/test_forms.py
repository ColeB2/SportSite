from django.test import TestCase
from league.models import Game, PlayerSeason, SeasonStage, TeamSeason
from stats.models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameStats, TeamGameLineScore)
from stats.forms import (PlayerStatsCreateForm, PlayerPitchingStatsCreateForm,
    LinescoreEditForm, PHGSFHelper, PlayerHittingGameStatsForm, PPGSFHelper, 
    PlayerPitchingGameStatsForm)



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


        