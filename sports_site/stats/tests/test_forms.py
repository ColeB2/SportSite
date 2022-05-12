from django.test import TestCase
from stats.models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameStats, TeamGameLineScore)
from stats.forms import (PlayerStatsCreateForm, PlayerPitchingStatsCreateForm,
    LinescoreEditForm, PHGSFHelper, PlayerHittingGameStatsForm, PPGSFHelper, 
    PlayerPitchingGameStatsForm)


class PlayerStatsCreateFormTest(TestCase):
    def test_create_game_form_labels(self):
        form = PlayerStatsCreateForm()
        form_labels = {"player": False}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        pass
        # t1 = TeamSeason.objects.get(id="1")
        # t2 = TeamSeason.objects.get(id="2")
        # ts_query = TeamSeason.objects.all()
        # date = datetime.datetime(2022, 5, 11)
        # time = datetime.time(17, 00)
        # form_data = {"home_team": t1, "away_team": t2,
        #     "date": date, "start_time": time}
        # form = CreateGameForm(data=form_data, team_queryset=ts_query)
        # self.assertTrue(form.is_valid())    