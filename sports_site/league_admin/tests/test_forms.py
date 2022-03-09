from django.test import TestCase
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