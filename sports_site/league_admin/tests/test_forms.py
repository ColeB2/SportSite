import datetime
from django.test import TestCase
from league.models import Game, TeamSeason
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


class EditGameFormTest(TestCase):
    def test_edit_game_form_labels(self):
        form = EditGameForm()
        form_labels = {"home_team": "Home", "away_team": "Visitor",
            "location": "Location", "date": "Date",
            "start_time": "Time", "home_score": "Home score",
            "away_score": "Away score"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

        print(form.model)

    def test_forms(self):
        t1 = TeamSeason.objects.get(id="1")
        t2 = TeamSeason.objects.get(id="2")
        date = datetime.datetime(2022, 5, 11)
        time = datetime.time(17, 00)

        form_data = {"home_team": t1, "away_team": t2,
            "date": date, "start_time": time, "home_score": 99, "away_score": 0}

        form = EditGameForm(data=form_data)
        self.assertTrue(form.is_valid())


class PlayerCreateFormTest(TestCase):
    def test_player_create_form_labels(self):
        form = PlayerCreateForm()
        form_labels = {"first_name": "First name", "last_name": "Last name",
            "birthdate": "Birthdate - YYYY-MM-DD format", "bats": "Bats",
            "throw": "Throw", "height_feet": "Height, feet ie, 5,6 etc.",
            "height_inches": "Height, inches ie 1,2,3... etc.",
            "weight": "Weight, lbs"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        form_data = {"first_name": "Firsty", "last_name": "Lasty",
            "birthdate": "1900-12-01", "bats": "Right", "throw": "Switch",
            "height_feet": 7, "height_inches": 11, "weight": 400}

        form = PlayerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class SeasonFormTest(TestCase):
    pass



