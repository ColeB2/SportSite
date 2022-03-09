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
        league_label = self.league_hitting_options._meta.get_field('league').verbose_name
        options_label = self.league_hitting_options._meta.get_field('stat_options').verbose_name
        self.assertEqual(league_label, "league")
        self.assertEqual(options_label, "stat options")

    def test_defaults(self):
        self.assertEqual(self.league_hitting_options.stat_options, LeagueHittingOptions.SIMPLE)

    def test_max_length(self):
        options_max_length = self.league_hitting_options._meta.get_field("stat_options").max_length
        self.assertEqual(options_max_length, 8)


class LeagueHittingStatsOptionsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.lho = LeagueHittingOptions.objects.create(league=cls.league)
        cls.lhso = LeagueHittingStatsOptions.objects.create(league=cls.league, league_options=cls.lho)


    def test_fk_points(self):
        self.assertEqual(self.lhso.league, self.league)
        self.assertEqual(self.lhso.league_options, self.lho)

    def test_labels(self):
        label_dict = {"league": "league", "league_options": "league options",
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
        for k,v in label_dict.items():
            label = self.lhso._meta.get_field(k).verbose_name
            self.assertEqual(label, v)

    def test_defaults(self):
        defaults_true = ["at_bats", "plate_appearances",
        "hits", "runs", "strikeouts", "walks",
        "singles", "doubles", "triples", "homeruns",
        "stolen_bases", "caught_stealing", "runs_batted_in",
        "hit_by_pitch", "sacrifice_flies", "sacrifice_bunts",
        "average", "on_base_percentage", "slugging_percentage",
        "on_base_plus_slugging", "reached_on_error",
        "fielders_choice", "intentional_walks", "left_on_base",
        "picked_off", "ground_into_double_play",
        "two_out_runs_batted_in"
        ]
        self.assertEqual(self.lhso.ordered_lineup, False)
        for stat_name in defaults_true:
            stat = self.lhso._meta.get_field(stat_name)
            self.assertEqual(stat.default, True)

