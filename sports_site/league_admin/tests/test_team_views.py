from django.test import TestCase
from django.urls import reverse

from league.models import League, Team, TeamSeason


class LATeamCreateViewTest(TestCase):
    """
    Tests league_admin_team_create_view
        from league_admin/views/team_views.py

    'teams/add',
    views.league_admin_team_create_view,
    name='league-admin-team-create'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/teams/add')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/teams/add')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_templates/team_create.html")

    
    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context["form"] is not None)


    def test_create_team(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        pre_len = Team.objects.filter(league=league).count()
        post = {"name": "Team Name", "place": "Place Name", "abbreviation": "ABR"}

        response = self.client.post(reverse("league-admin-team-create"),
            post,
            follow=True)

        post_len = Team.objects.filter(league=league).count()
        self.assertEqual(pre_len+1, post_len)

    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)
        
        post = {"name": "Team Name", "place": "Place Name", "abbreviation": "ABR"}

        response = self.client.post(reverse("league-admin-team-create"),
            post,
            follow=True)

        self.assertRedirects(response, reverse("league-admin-dashboard"))


class LATeamEditViewTest(TestCase):
    """
    Tests league_admin_team_edit_view
        from league_admin/views/team_views.py

    'teams/team/<team_pk>/edit',
        views.league_admin_team_edit_view,
        name="league-admin-team-edit"
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.league = League.objects.get(id=1)
        cls.team = Team.objects.create(league=cls.league, name="TName",
            place="TPlace",
            abbreviation="TNT")
        return super().setUpTestData()

    def test_view_without_logging_in(self):
        response = self.client.get(f'/league/admin/teams/team/{self.team.pk}/edit')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(f'/league/admin/teams/team/{self.team.pk}/edit')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-edit",
            kwargs = {"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-edit",
            kwargs = {"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_templates/team_edit.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-edit",
            kwargs = {"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)


        self.assertTrue(response.context["form"] is not None)
        self.assertEqual(response.context["team_instance"], self.team)
        self.assertEqual(response.context["league"], self.league)


    def test_edit_team(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-edit",
            kwargs = {"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)

        name="New Name"
        place="New Place"
        abbr = "NNN"

        post = {"name": name, "place": place, "abbreviation": abbr}
        self.assertEqual(self.team.name, "TName")

        response = self.client.post(reverse("league-admin-team-edit",
            kwargs = {"team_pk": self.team.pk}),
            post,
            follow=True)


        team_edit = Team.objects.get(id=self.team.id)
        self.assertEqual(team_edit.name, name)
        self.assertEqual(team_edit.place, place)
        self.assertEqual(team_edit.abbreviation, abbr)


    
    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-create"))
        self.assertEqual(response.status_code, 200)
        
        post = {"name": "Team Name", "place": "Place Name", "abbreviation": "ABR"}

        response = self.client.post(reverse("league-admin-team-edit",
            kwargs = {"team_pk": self.team.pk}),
            post,
            follow=True)

        self.assertRedirects(response, reverse("league-admin-team-info",
            kwargs={"team_pk": self.team.pk}))

        

class LATeamSelectViewTest(TestCase):
    """
    Tests league_admin_team_select_view
        from league_admin/views/team_views.py

    'teams/',
    views.league_admin_team_select_view,
    name='league-admin-team-select'
    """
    def test_view_without_logging_in(self):
        response = self.client.get(f'/league/admin/teams/')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(f'/league/admin/teams/')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-select"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_templates/team_select.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-select"))
        self.assertEqual(response.status_code, 200)


        league = League.objects.get(id=1)
        teams = Team.objects.filter(league=league)
        self.assertQuerysetEqual(response.context["teams"], teams, ordered=False)



class LATeamSelectViewTest(TestCase):
    """
    Tests league_admin_team_info_view
        from league_admin/views/team_views.py

    'teams/team/<int:team_pk>',
    views.league_admin_team_info_view,
    name="league-admin-team-info"
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.league = League.objects.get(id=1)
        cls.team = Team.objects.create(league=cls.league, name="TName",
            place="TPlace",
            abbreviation="TNT")
        return super().setUpTestData()


    def test_view_without_logging_in(self):
        response = self.client.get(f'/league/admin/teams/team/{self.team.pk}')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(f'/league/admin/teams/team/{self.team.pk}')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-info", 
            kwargs={"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-info", 
            kwargs={"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_templates/team_page.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-info", 
            kwargs={"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)


        team_seasons = TeamSeason.objects.filter(team=self.team)
        self.assertEqual(response.context["team"], self.team)
        self.assertQuerysetEqual(
            response.context["team_seasons"],
            team_seasons,
            ordered=False)


class LATeamSelectViewTest(TestCase):
    """
    Tests league_admin_team_delete_info_view
        from league_admin/views/team_views.py

    'teams/team/<int:team_pk>/delete',
    views.league_admin_team_delete_info_view,
    name='league-admin-team-delete'
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.league = League.objects.get(id=1)
        cls.team = Team.objects.create(league=cls.league, name="TName",
            place="TPlace",
            abbreviation="TNT")
        return super().setUpTestData()


    def test_view_without_logging_in(self):
        response = self.client.get(
            f'/league/admin/teams/team/{self.team.pk}/delete')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(
            f'/league/admin/teams/team/{self.team.pk}/delete')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-delete", 
            kwargs={"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-delete", 
            kwargs={"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/team_templates/team_delete.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-team-delete", 
            kwargs={"team_pk": self.team.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["team"], self.team)
        self.assertTrue(response.context["nested_object"] is not None)


    def test_delete(self):
        teams_count = Team.objects.filter(league=self.league).count()

        self.client.login(username="Test", password="test")
        response = self.client.post(reverse("league-admin-team-delete", 
            kwargs={"team_pk": self.team.pk}),
            follow=True)

        self.assertRedirects(response,
            reverse("league-admin-team-select"))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{self.team} and all related objects were deleted.')

        teams_count_del = Team.objects.filter(league=self.league).count()

        self.assertEqual(teams_count - 1, teams_count_del)


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse("league-admin-team-delete", 
            kwargs={"team_pk": self.team.pk}),
            follow=True)

        self.assertRedirects(response,
            reverse("league-admin-team-select"))