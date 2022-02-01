from django.test import TestCase
from django.contrib.auth.models import User
from league.models import Player, PlayerSeason, Season, SeasonStage, League
from league.models import PlayerSeason

# Create your tests here.
class StatsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="Test", email="test@email.com", password="test")
        cls.league = League.objects.create(name="Test League", admin=cls.user, url="TL")

    def test_herehere(self):
        print(self.league)
        self.assertEqual(1,1)

