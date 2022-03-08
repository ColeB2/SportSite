from django.test import TestCase
from league_admin.models import LeagueHittingOptions, LeagueHittingStatsOptions
from league.models import League


class LeagueHittingOptionsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.league_hitting_options = LeagueHittingOptions.objects.create(league=cls.league)

    def test_created_properly(self):
        self.assertEqual(self.league_hitting_options.league, self.league)
        self.assertEqual(self.league_hitting_options.stat_options, LeagueHittingOptions.SIMPLE)

    def test_fk_points(self):
        self.assertEqual(self.league_hitting_options.league, self.league)

    def test_labels(self):
        league_label = self.league_hitting_optins._meta.get_field('league').verbose_name
        options_label = self.league_hitting_optins._meta.get_field('stat_options').verbose_name
        self.assertEqual(league_label, "league")
        self.assertEqual(options_label, "stat options")

    def test_defaults(self):
        self.assertEqual(self.league_hitting_options.stat_options, LeagueHittingOptions.SIMPLE)

    def test_max_length(self):
        options_max_length = self.league_hitting_options._meta.get_field("stat_options").max_length
        self.assertEqual(options_max_length, 8)
