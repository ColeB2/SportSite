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
        return temp_return

    def teardown_databases(self, *args, **kwargs):
        return super(MyMixinRunner, self).teardown_databases(*args, **kwargs)

class MyTestRunner(MyMixinRunner, BaseRunner):
    pass



class LeagueTestCase(TestCase):
    def setUp(self):
        self.league = League.objects.get(id=1)

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
    def setUp(self):
        self.league = League.objects.get(id=1)
        self.season = Season.objects.get(id=1)

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
    def setUp(self):
        self.league = League.objects.get(id=1)
        self.season = Season.objects.get(id=1)
        self.regular = SeasonStage.objects.get(stage=SeasonStage.REGULAR)
        self.post = SeasonStage.objects.get(stage=SeasonStage.POST)
        self.other = SeasonStage.objects.get(stage=SeasonStage.OTHER)

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
        self.assertEqual(field_label, 'stage_name')

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


