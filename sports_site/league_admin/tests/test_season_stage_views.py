from django.test import TestCase
from django.urls import reverse

from league.models import League, Season, SeasonStage, Team, TeamSeason


class LASeasonStageSelectViewTest(TestCase):
    """
    Tests league_admin_season_stage_select_view
        from league_admin/views/season_stage_views.py

    'season/<int:season_year>/<season_pk>',
    views.league_admin_season_stage_select_view,
    name='league-admin-season-stage'),
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": 2022, "season_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": 2022, "season_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_select_page.html")


    def test_context(self):
        season_year = 2022
        season_pk = 1
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": season_year, "season_pk": season_pk}))
        self.assertEqual(response.status_code, 200)

        season = Season.objects.get(pk=season_pk)
        stages = SeasonStage.objects.filter(season=season)

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season"], season)
        self.assertQuerysetEqual(
            response.context["stages"], stages, ordered=False)



class LASeasonStageCreateViewTest(TestCase):
    """
    Tests league_admin_season_stage_create_view
        from league_admin/views/season_stage_views.py

    'season/<int:season_year>/<season_pk>/add/new',
    views.league_admin_season_stage_create_view,
    name='league-admin-season-stage-create')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/add/new')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/add/new')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-create",
            kwargs={"season_year": 2022, "season_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-create",
            kwargs={"season_year": 2022, "season_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_create.html")


    
    def test_context(self):
        season_year = 2022
        season_pk = 1
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-create",
            kwargs={"season_year": season_year, "season_pk": season_pk}))
        self.assertEqual(response.status_code, 200)

        season = Season.objects.get(pk=season_pk)
        stages = SeasonStage.objects.filter(season=season)

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season"], season)
        self.assertQuerysetEqual(
            response.context["stages"], stages, ordered=False)
        self.assertTrue(response.context["form"] is not None)
        self.assertTrue(response.context["formset"] is not None)


    def test_redirects(self):
        season_year = 2022
        season_pk = 1
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-create",
            kwargs={"season_year": season_year, "season_pk": season_pk}))
        self.assertEqual(response.status_code, 200)


        season = Season.objects.get(pk=season_pk)
        stages = SeasonStage.objects.filter(season=season)
        t1 = Team.objects.get(id=1)
        t2 = Team.objects.get(id=2)

        stage_data = {
            "stage": SeasonStage.REGULAR,
            "id_form-0-teams": t1,
            "id_form-1-teams": 2,
            "id_form-2-teams": {"value": 2},
            "form-0-teams": t1,
            "form-1-teams": 2,
            "form-2-teams": {"value": 2},
        }
        team_data = {
            "form-1-teams": t1,
            "form-2-teams": t2
        }

        resp = self.client.post(reverse("league-admin-season-stage-create",
            kwargs={"season_year": season_year, "season_pk": season_pk}),
            stage_data,
            follow=True
            )

        print("ToDo: season_stage_tests: Figure how to pass data to formsets")
        self.assertRedirects(resp, reverse("league-admin-season-stage",
            kwargs={"season_year": season_year, "season_pk": season_pk}))



class LASeasonStageInfoViewTest(TestCase):
    """
    Tests league_admin_season_stage_info_view
        from league_admin/views/season_stage_views.py

    'season/<int:season_year>/<season_pk>/<season_stage_pk>',
    views.league_admin_season_stage_info_view,
    name='league-admin-season-stage-info')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/3')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/3')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-info",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-info",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_page.html")


    
    def test_context(self):
        season_year = 2022
        season_pk = 1
        season_stage_pk = 3
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-info",
            kwargs={"season_year": season_year, "season_pk": season_pk,
                "season_stage_pk": season_stage_pk}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=season_stage_pk)
        teams = TeamSeason.objects.filter(team__league=League.objects.get(id=1),
                                          season__pk=season_stage_pk)

        self.assertEqual(response.context["stage"], stage)
        self.assertQuerysetEqual(
            response.context["teams"], teams, ordered=False)



class LASeasonStageDeleteInfoViewTest(TestCase):
    """
    Tests league_admin_season_stage_delete_info_view
        from league_admin/views/season_stage_views.py

    'season/<int:season_year>/<season_pk>/<season_stage_pk>/delete',
    views.league_admin_season_stage_delete_info_view,
    name='league-admin-season-stage-delete')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/3/delete')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/3/delete')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-delete",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-delete",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_delete.html")


    def test_context(self):
        season_year = 2022
        season_pk = 1
        season_stage_pk = 3
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-delete",
            kwargs={"season_year": season_year, "season_pk": season_pk,
                "season_stage_pk": season_stage_pk}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=season_stage_pk)
        teams = TeamSeason.objects.filter(team__league=League.objects.get(id=1),
                                          season__pk=season_stage_pk)


        self.assertEqual(response.context["stage"], stage)
        self.assertTrue(response.context["nested_object"] is not None)


    def test_season_stage_delete(self):
        sslen = len(SeasonStage.objects.all())
        s = Season.objects.get(id=1)
        ss = SeasonStage.objects.create(season=s, stage=SeasonStage.REGULAR)
        self.assertEqual(len(SeasonStage.objects.all()), sslen+1)

        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-delete",
            kwargs={"season_year": ss.season.year, "season_pk": s.pk,
                "season_stage_pk": ss.pk}))
        self.assertEqual(response.status_code, 200)

        resp = self.client.post(reverse("league-admin-season-stage-delete",
            kwargs={"season_year": ss.season.year, "season_pk": s.pk,
                "season_stage_pk": ss.pk}), follow=True)

        self.assertRedirects(resp, reverse(
            "league-admin-season-stage",
            kwargs={"season_year":s.year, "season_pk": s.pk}))
        len_season_stage = len(SeasonStage.objects.all())
        self.assertEqual(len_season_stage, sslen)


class LASeasonStageAddTeamsViewTests(TestCase):
    """
    Tests league_admin_season_stage_add_teams_view
        from league_admin/views/season_stage_views.py

    'season/<int:season_year>/<season_pk>/<season_stage_pk>/add/teams',
    views.league_admin_season_stage_add_teams_view,
    name='league-admin-season-stage-add-teams')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/3/add/teams')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/3/add/teams')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-add-teams",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-add-teams",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_add_teams.html")


    def test_context(self):
        season_year = 2022
        season_pk = 1
        season_stage_pk = 3
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-add-teams",
            kwargs={"season_year": season_year, "season_pk": season_pk,
                "season_stage_pk": season_stage_pk}))
        self.assertEqual(response.status_code, 200)

        season = Season.objects.get(pk=season_pk)
        stage = SeasonStage.objects.get(pk=season_stage_pk)
        teams = Team.objects.filter(league=League.objects.get(id=1))
        exist_teams = TeamSeason.objects.filter(season__pk=season_stage_pk)


        self.assertEqual(response.context["season"], season)
        self.assertEqual(response.context["season_year"], season_year)
        self.assertEqual(response.context["stage"], stage)
        self.assertQuerysetEqual(
            response.context["teams"], exist_teams, ordered=False)
        self.assertTrue(response.context["formset"] is not None)



class LASeasonStageSetFeaturedViewTests(TestCase):
    """
    Tests league_admin_season_stage_set_featured_view
        from league_admin/views/season_stage_views.py

    'season/<int:season_year>/<season_pk>/<season_stage_pk>/make-featured',
    views.league_admin_season_stage_set_featured_view,
    name='league-admin-season-stage-featured'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/3/make-featured')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/3/make-featured',
            follow=True)
        self.assertRedirects(response, reverse(
            "league-admin-season-stage-info",
            kwargs={"season_year":2022, "season_pk":1, "season_stage_pk":3}))
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-featured",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": "3"}),
                follow=True)
        self.assertRedirects(response, reverse(
            "league-admin-season-stage-info",
            kwargs={"season_year":2022, "season_pk":1, "season_stage_pk":3}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        """Redirect only view, so tests template after redirect"""
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-featured",
            kwargs={"season_year": 2022, "season_pk": 1,
                "season_stage_pk": "3"}),
                follow=True)
        self.assertRedirects(response, reverse(
            "league-admin-season-stage-info",
            kwargs={"season_year":2022, "season_pk":1, "season_stage_pk":3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_page.html")


    def test_makes_featured(self):
        season_year = 2022
        season_pk = 1
        season_stage_pk = 1
        stage = SeasonStage.objects.get(pk=season_stage_pk)
        self.assertEqual(stage.featured, False)
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-featured",
            kwargs={"season_year": 2022, "season_pk": season_pk,
                "season_stage_pk": season_stage_pk}),
                follow=True)

        stage = SeasonStage.objects.get(pk=season_stage_pk)
        self.assertEqual(stage.featured, True)

        


        




