import datetime
from django.test import TestCase
from league.models import TeamSeason
from league_admin.forms import (CreateGameForm, EditGameForm,
    LeagueHittingOptionsForm, LeagueHittingStatsOptionsForm,
    PlayerCreateForm, SeasonForm, SeasonStageCreateForm, TeamCreateForm,
    TeamSelectForm)


class CreateGameFormTest(TestCase):
    def test_create_game_form_labels(self):
        form = CreateGameForm()
        form_labels = {"home_team": "Home team", "away_team": "Away team",
            "location": "Location (default: Home)", "date": None,
            "start_time": "Start Time (24:00 clock)"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        t1 = TeamSeason.objects.get(id="1")
        t2 = TeamSeason.objects.get(id="2")
        ts_query = TeamSeason.objects.all()
        date = datetime.datetime(2022, 5, 11)
        time = datetime.time(17, 00)
        form_data = {"home_team": t1, "away_team": t2,
            "date": date, "start_time": time}

        form = CreateGameForm(data=form_data, team_queryset=ts_query)
        self.assertTrue(form.is_valid())