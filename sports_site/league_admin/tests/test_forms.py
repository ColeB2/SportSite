import datetime
from django.test import TestCase
from league.models import Game, League, SeasonStage, TeamSeason
from league_admin.models import LeagueHittingOptions
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


    def test_forms(self):
        t1 = TeamSeason.objects.get(id="1")
        t2 = TeamSeason.objects.get(id="2")
        date = datetime.datetime(2022, 5, 11)
        time = datetime.time(17, 00)

        form_data = {"home_team": t1, "away_team": t2,
            "date": date, "start_time": time, "home_score": 99, "away_score": 0}

        form = EditGameForm(data=form_data)
        self.assertTrue(form.is_valid())



class LeagueHittingOptionsFormTest(TestCase):
    def test_league_hitting_options_form_labels(self):
        form = LeagueHittingOptionsForm()
        form_labels = {"stat_options": "Stat options"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        form_data = {"stat_options": LeagueHittingOptions.ADVANCED}
        form = LeagueHittingOptionsForm(data=form_data)

        self.assertTrue(form.is_valid())



class LeagueHittingStatsOptionsFormTest(TestCase):
    def test_league_hitting_stats_options_form_labels(self):
        #WIP as we implemented actual options
        form = LeagueHittingStatsOptionsForm()
        form_labels = {
        "ordered_lineup": "Ordered", "at_bats": "AB", "plate_appearances": "PA",
        "hits": "H", "runs": "R", "strikeouts": "SO", "walks": "BB",
        "singles": "1B", "doubles": "2B", "triples": "3B", "homeruns": "HR",
        "stolen_bases": "SB", "caught_stealing": "CS", "runs_batted_in": "RBI",
        "hit_by_pitch": "HBP", "sacrifice_flies": "SF", "sacrifice_bunts": "SAC",
        "average": "AVG", "on_base_percentage": "OBP", "slugging_percentage": "SLG",
        "on_base_plus_slugging": "OPS", "reached_on_error": "ROE",
        "fielders_choice": "FC", "intentional_walks": "IBB", "left_on_base": "LOB",
        "picked_off": "PO", "ground_into_double_play": "GIDP",
        "two_out_runs_batted_in": "2-out-RBI"
        }

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        #WIP
        league = League.objects.get(id="1")
        lho = LeagueHittingOptions.objects.create(league=league, stat_options=LeagueHittingOptions.ADVANCED)
        form_data = {"league": league, "league_options": lho}
        form = LeagueHittingStatsOptionsForm(data=form_data)
        self.assertTrue(form.is_valid())


class PlayerCreateFormTest(TestCase):
    def test_player_create_form_labels(self):
        form = PlayerCreateForm()
        form_labels = {"first_name": "First name", "last_name": "Last name",
            "birthdate": "Birthdate - YYYY-MM-DD format", "bats": "Bats",
            "throw": "Throw", "height_feet": "Height, feet, ie 5,6, etc.",
            "height_inches": "Height, inches, ie 1,2,3... etc.",
            "weight": "Weight, lbs"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            #print(label, v)
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        form_data = {"first_name": "Firsty", "last_name": "Lasty",
            "birthdate": "1900-12-01", "bats": "Right", "throw": "Switch",
            "height_feet": 7, "height_inches": 11, "weight": 400}

        form = PlayerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class SeasonFormTest(TestCase):
    def test_season_form_labels(self):
        form = SeasonForm()
        form_labels = {"year": "Year"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        form_data = {"year": "2222"}
        form = SeasonForm(data = form_data)

        self.assertTrue(form.is_valid())


class SeasonStageCreateFormTest(TestCase):
    def test_season_stage_create_labels(self):
        form = SeasonStageCreateForm()
        form_labels = {"stage": "Stage", "stage_name": "Stage name",
            "featured": "Featured"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            self.assertTrue(label is None or label == v)

    def test_forms(self):
        form_data = {"stage": SeasonStage.REGULAR, "stage_name": "",
            "featured": True}
        form = SeasonStageCreateForm(data=form_data)

        self.assertTrue(form.is_valid())


class TeamCreateFormTest(TestCase):
    def test_team_create_form_labels(self):
        form = TeamCreateForm()
        form_labels = {"name": "Name", "place": "Place",
            "abbreviation": "Abbreviation"}

        for k,v in form_labels.items():
            label = form.fields[k].label
            # print(label, v)
            self.assertTrue(label is None or label == v)


    def test_forms(self):
        form_data = {"name": "NameOne", "place": "PlaceOne",
            "abbreviation": "NOP"}

        form = TeamCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class TeamSelectFormTest(TestCase):
    #No Labels...
    def test_forms(self):
        t1 = TeamSeason.objects.get(id="1")
        t2 = TeamSeason.objects.get(id="2")
        ts_query = TeamSeason.objects.all()

        form_data = {"teams": t1}
        form = TeamSelectForm(data=form_data, team_queryset=ts_query)
        self.assertTrue(form.is_valid())





