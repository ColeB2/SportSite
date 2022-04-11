from django.test import TestCase
from django.urls import reverse

from league.models import TeamSeason


class LATeamSeasonInfoViewTest(TestCase):
    """
    Tests league_admin_team_season_info_view
        from league_admin/views/team_season_views.py

    'season/<int:season_year>/<int:season_pk>/<int:season_stage_pk>/<team_name>/
        <team_season_pk>',
    views.league_admin_team_season_info_view,
    name='league-admin-team-season-info'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/3/TeamOne/1')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/3/TeamOne/1')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-season-info",
            kwargs={
                "season_year": 2022, "season_pk": 1, "season_stage_pk":3,
                "team_name": "TeamOne", "team_season_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-season-info",
            kwargs={
                "season_year": 2022, "season_pk": 1, "season_stage_pk":3,
                "team_name": "TeamOne", "team_season_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_season_templates/team_season_info.html")


    def test_context(self):
        context = {"season_year": 2022, "season_pk": 1, "season_stage_pk":3,
                "team_name": "TeamOne", "team_season_pk": 1}

        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-season-info",
            kwargs={
                "season_year": context["season_year"],
                "season_pk": context["season_pk"],
                "season_stage_pk": context["season_stage_pk"], 
                "team_name": context["team_name"],
                "team_season_pk": context["team_season_pk"]}))
        self.assertEqual(response.status_code, 200)

        team = TeamSeason.objects.get(pk=context["team_season_pk"])
        roster = team.roster_set.get(team__pk=context["team_season_pk"])
        players = roster.playerseason_set.all()

        self.assertEqual(response.context["season_year"], context["season_year"])
        self.assertEqual(response.context["season_pk"], context["season_pk"])
        self.assertEqual(response.context["season_stage_pk"], context["season_stage_pk"])
        self.assertEqual(response.context["team_name"], context["team_name"])
        self.assertEqual(response.context["team"], team)
        self.assertEqual(response.context["roster"], roster)
        self.assertQuerysetEqual(
            response.context["players"], players, ordered=False)