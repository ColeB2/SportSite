from django.test import TestCase
from league.models import Game, SeasonStage, TeamSeason
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

        