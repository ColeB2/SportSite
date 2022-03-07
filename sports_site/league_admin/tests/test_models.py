from django.test import TestCase
from league_admin.models import LeagueHittingOptions, LeagueHittingStatsOptions
from league.models import League


class LeagueHittingOptionsTestCase(TestCase):
    @classmethod
    def setUpTestaData(cls):
        cls.league = League.objects.get(id=1)
        cls.league_hitting_options = LeagueHittingOptions.create(league=league)

    def test_created_properly(self):
        self.assertEqual(self.league_hitting_options.league, self.league)
        self.assertEqual(self.league_hitting_options.stat_options, LeagueHittingOptions.SIMPLE)