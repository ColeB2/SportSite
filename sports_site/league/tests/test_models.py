from django.test import TestCase
from league.models import (Game, League, Player, PlayerSeason, Roster, Season,
    SeasonStage, Team, TeamSeason)
from django.contrib.auth.models import User

from django.test.runner import DiscoverRunner as BaseRunner

class MyMixinRunner(object):
    def setup_databases(self, *args, **kwargs):
        temp_return = super(MyMixinRunner, self).setup_databases(*args, **kwargs)
        user = User.objects.create(username="Test", email="test@email.com", password="test")
        league = League.objects.create(name="Test League", admin=user, url="TL")
        season = Season.objects.create(year="2022", league=league)

        stageO = SeasonStage.objects.create(stage=SeasonStage.OTHER, season=season, stage_name="Preseason", featured=True)
        stageP = SeasonStage.objects.create(stage=SeasonStage.POST, season=season, featured=True)
        stageR = SeasonStage.objects.create(stage=SeasonStage.REGULAR, season=season, featured=True)

        team1 = Team.objects.create(owner=user, league=league, name="Team One", place="Town One", abbreviation="TTO")
        team2 = Team.objects.create(owner=user, league=league, name="Team Two", place="Town Two", abbreviation="TTT")

        team1r = TeamSeason.objects.create(season=stageR, team=team1)
        roster1 = Roster.objects.get(team=team1r)
        team2r = TeamSeason.objects.create(season=stageR, team=team2)

        player11 = Player.objects.create(league=league, first_name="Player", last_name="One")
        player21 = Player.objects.create(league=league, first_name="Player", last_name="Two")

        playerseason11 = PlayerSeason.objects.create(player=player11, team=roster1, season=stageR, number=99, position="CF")


        return temp_return

    def teardown_databases(self, *args, **kwargs):
        return super(MyMixinRunner, self).teardown_databases(*args, **kwargs)

class MyTestRunner(MyMixinRunner, BaseRunner):
    pass



class LeagueTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)

    def test_created_properly(self):
        self.assertEqual(self.league.name, "Test League")

    def test_name_label(self):
        field_label = self.league._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_url_slug_label(self):
        field_label = self.league._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')

    def test_name_max_length(self):
        max_length = self.league._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_url_slug_max_length(self):
        max_length = self.league._meta.get_field('url').max_length
        self.assertEqual(max_length, 25)

    def test_expected_name(self):
        expected_name = f"{self.league.name}"
        self.assertEqual(str(self.league), expected_name)


class SeasonTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.season = Season.objects.get(id=1)

    def test_created_properly(self):
        self.assertEqual(self.season.year, "2022")

    def test_season_in_proper_league(self):
        self.assertEqual(self.season.league, self.league)

    def test_year_label(self):
        field_label = self.season._meta.get_field('year').verbose_name
        self.assertEqual(field_label, 'year')

    def test_year_max_length(self):
        max_length = self.season._meta.get_field('year').max_length
        self.assertEqual(max_length, 10)

    def test_expected_name(self):
        expected_name = f"{self.season.year}"
        self.assertEqual(str(self.season), expected_name)


class SeasonStageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.season = Season.objects.get(id=1)
        cls.regular = SeasonStage.objects.get(stage=SeasonStage.REGULAR)
        cls.post = SeasonStage.objects.get(stage=SeasonStage.POST)
        cls.other = SeasonStage.objects.get(stage=SeasonStage.OTHER)

    def test_created_properly(self):
        self.assertEqual(self.regular.stage, SeasonStage.REGULAR)
        self.assertEqual(self.post.stage, SeasonStage.POST)
        self.assertEqual(self.other.stage, SeasonStage.OTHER)

    def test_season_stage_point_proper_season(self):
        self.assertEqual(self.regular.season, self.season)
        self.assertEqual(self.post.season, self.season)
        self.assertEqual(self.other.season, self.season)

    def test_stage_name_label(self):
        field_label = self.other._meta.get_field('stage_name').verbose_name
        self.assertEqual(field_label, 'stage name')

    def test_stage_name_max_length(self):
        max_length = self.other._meta.get_field('stage_name').max_length
        self.assertEqual(max_length, 50)

    def test_stage_label(self):
        field_label = self.other._meta.get_field('stage').verbose_name
        self.assertEqual(field_label, 'stage')

    def test_stage_max_length(self):
        max_length = self.other._meta.get_field('stage').max_length
        self.assertEqual(max_length, 20)

    def test_featured_label(self):
        field_label = self.other._meta.get_field('featured').verbose_name
        self.assertEqual(field_label, 'Featured')

    def test_proper_featured(self):
        #regular created last, should be featured.
        self.assertEqual(self.regular.featured, True)
        self.assertEqual(self.post.featured, False)
        self.assertEqual(self.other.featured, False)

    def test_expected_name(self):
        self.assertEqual(str(self.regular), "2022 Regular Season")
        self.assertEqual(str(self.post), "2022 Postseason")
        self.assertEqual(str(self.other), "2022 Preseason")


class TeamTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.team1 = Team.objects.get(name="Team One")
        cls.team2 = Team.objects.get(name="Team Two")
        cls.teamtest = Team.objects.create(name="Team Onee", place="Town One")

    def test_created_properly(self):
        self.assertEqual(self.team1.name, "Team One")
        self.assertEqual(self.team2.name, "Team Two")
        self.assertEqual(self.team1.place, "Town One")
        self.assertEqual(self.team2.place, "Town Two")
        self.assertEqual(self.team1.abbreviation, "TTO")
        self.assertEqual(self.team2.abbreviation, "TTT")

    def test_points_to_proper_league(self):
        self.assertEqual(self.team1.league, self.league)
        self.assertEqual(self.team2.league, self.league)

    def test_name_label(self):
        field_label = self.team1._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_place_label(self):
        field_label = self.team1._meta.get_field('place').verbose_name
        self.assertEqual(field_label, 'place')

    def test_abbreviation_label(self):
        field_label = self.team1._meta.get_field('abbreviation').verbose_name
        self.assertEqual(field_label, 'abbreviation')

    def test_unique_abbreviation(self):
        #check test
        self.assertEqual(self.teamtest.abbreviation, "TOW")

    def test_name_max_length(self):
        max_length = self.team1._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_place_max_length(self):
        max_length = self.team1._meta.get_field('place').max_length
        self.assertEqual(max_length, 30)

    def test_abbreviation_max_length(self):
        max_length = self.team1._meta.get_field('abbreviation').max_length
        self.assertEqual(max_length, 3)

    def test_expected_name(self):
        self.assertEqual(str(self.team1), "Town One Team One")
        self.assertEqual(str(self.team2), "Town Two Team Two")


class TeamSeasonTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(stage=SeasonStage.REGULAR, featured=True)
        cls.team1 = Team.objects.get(name="Team One")
        cls.team2 = Team.objects.get(name="Team Two")
        cls.team1r = TeamSeason.objects.get(team=cls.team1)
        cls.team2r = TeamSeason.objects.get(team=cls.team2)

    def test_points_proper_team_and_stage(self):
        self.assertEqual(self.team1r.team, self.team1)
        self.assertEqual(self.team1r.season, self.stage)

    def test_expected_name(self):
        self.assertEqual(str(self.team1r), "Town One Team One 2022 Regular Season")
        self.assertEqual(str(self.team2r), "Town Two Team Two 2022 Regular Season")

    def test_roster_created(self):
        roster1 = self.team1r.roster_set.all()[0]
        self.assertEqual(roster1.team, self.team1r)

class RosterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.team1 = Team.objects.get(name="Team One")
        cls.team1r = TeamSeason.objects.get(team=cls.team1)
        cls.roster1 = Roster.objects.get(team__team__name="Team One")

    def test_points_proper_teamseason(self):
        self.assertEqual(self.roster1.team, self.team1r)

    def test_expected_name(self):
        self.assertEqual(str(self.roster1), "Town One Team One 2022 Regular Season")


class PlayerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.player1 = Player.objects.get(league=cls.league, last_name="One")
        cls.player2 = Player.objects.get(league=cls.league, last_name="Two")

    def test_points_proper_league(self):
        self.assertEqual(self.player1.league, self.league)
        self.assertEqual(self.player2.league, self.league)

    def test_first_name_label(self):
        field_label = self.player1._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        field_label = self.player1._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_birthdate_label(self):
        field_label = self.player1._meta.get_field('birthdate').verbose_name
        self.assertEqual(field_label, 'birthdate')

    def test_bats_label(self):
        field_label = self.player1._meta.get_field('bats').verbose_name
        self.assertEqual(field_label, 'bats')

    def test_throw_label(self):
        field_label = self.player1._meta.get_field('throw').verbose_name
        self.assertEqual(field_label, 'throw')

    def test_height_feet_label(self):
        field_label = self.player1._meta.get_field('height_feet').verbose_name
        self.assertEqual(field_label, 'height feet')

    def test_height_inches_label(self):
        field_label = self.player1._meta.get_field('height_inches').verbose_name
        self.assertEqual(field_label, 'height inches')

    def test_weight_label(self):
        field_label = self.player1._meta.get_field('weight').verbose_name
        self.assertEqual(field_label, 'weight')

    def test_expected_name(self):
        self.assertEqual(str(self.player1), "One, Player")
        self.assertEqual(str(self.player2), "Two, Player")

    def test_full_name(self):
        self.assertEqual(self.player1.full_name, "Player One")
        self.assertEqual(self.player2.full_name, "Player Two")

    def test_first_name_max_length(self):
        max_length = self.player1._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 35)

    def test_last_name_max_length(self):
        max_length = self.player1._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 35)


class PlayerSeasonTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.player = Player.objects.get(league=cls.league, first_name="Player", last_name="One")
        cls.pseason = PlayerSeason.objects.get(player=cls.player)
        cls.stage = SeasonStage.objects.get(stage=SeasonStage.REGULAR, featured=True)
        cls.roster = Roster.objects.get(team__team__name="Team One", team__season=cls.stage)

    def test_fk_point_proper_place(self):
        self.assertEqual(self.pseason.player, self.player)
        self.assertEqual(self.pseason.team, self.roster)
        self.assertEqual(self.pseason.season, self.stage)

    def test_labels(self):
        player_label = self.pseason._meta.get_field('player').verbose_name
        team_label = self.pseason._meta.get_field('team').verbose_name
        season_label = self.pseason._meta.get_field('season').verbose_name
        num_label = self.pseason._meta.get_field('number').verbose_name
        pos_label = self.pseason._meta.get_field('position').verbose_name
        self.assertEqual(player_label, 'player')
        self.assertEqual(team_label, 'team')
        self.assertEqual(season_label, 'season')
        self.assertEqual(num_label, 'number')
        self.assertEqual(pos_label, 'position')


    def test_expected_name(self):
        self.assertEqual(str(self.pseason), "One, Player 2022 Regular Season")





