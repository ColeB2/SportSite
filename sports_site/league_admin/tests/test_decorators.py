from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from mock import Mock

from league_admin.decorators import (user_owns_season_stage, user_owns_player,
    user_owns_season, user_owns_team, user_owns_team_season, user_logged_in)


class DecoratorTesting(TestCase):
    """
    Tests league_admin decorators.py decorators

    Improve.
    """
    def setUp(self):
        self.user = User.objects.create(username="foo", password="bar")
        self.factory = RequestFactory()

    def test_user_owns_season_stage_bad(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse("league-admin-season-stage-delete",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 403)

    
    def test_user_owns_season_bad(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse("league-admin-season-delete",
            kwargs={"season_year": 2020,
                    "season_pk": 1}))
        self.assertEqual(response.status_code, 403)

    
    def test_user_owns_player_bad(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse("league-admin-player-delete",
            kwargs={"player_pk": 1}))
        self.assertEqual(response.status_code, 403)

    
    def test_user_owns_team_bad(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse("league-admin-team-delete", 
            kwargs={"team_pk": 1}))
        self.assertEqual(response.status_code, 403)


    def test_user_owns_team_season_bad(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse("league-admin-team-season-info",
            kwargs={
                "season_year": 2022, "season_pk": 1, "season_stage_pk":3,
                "team_name": "Team One", "team_season_pk": 1}))
        self.assertEqual(response.status_code, 403)


    def test_user_logged_in_bad(self):
        response = self.client.get(reverse("league-admin-options"))
        self.assertEqual(response.status_code, 403)

    
