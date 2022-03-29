from django.test import TestCase
from django.urls import reverse

from league.models import Season, SeasonStage, Team, TeamSeason


class LASeasonStageSelectViewTest(TestCase):
    """
    Tests league_admin_season_stage_select_view
        from league_admin/views/schedule_views.py

    'season/<int:season_year>/<season_pk>',
    views.league_admin_season_stage_select_view,
    name='league-admin-season-stage'),
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": 2022, "season_pk": "1"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage",
            kwargs={"season_year": 2022, "season_pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_select_page.html")


    def test_context(self):
        season_year = 2022
        season_pk = 1
        login = self.client.login(username="Test", password="test")
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
    Tests league_admin_season_stage_createt_view
        from league_admin/views/schedule_views.py

    'season/<int:season_year>/<season_pk>/add/new',
    views.league_admin_season_stage_create_view,
    name='league-admin-season-stage-create')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/2022/1/add/new')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/2022/1/add/new')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-create",
            kwargs={"season_year": 2022, "season_pk": "1"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-stage-create",
            kwargs={"season_year": 2022, "season_pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_stage_templates/season_stage_create.html")


    
    def test_context(self):
        season_year = 2022
        season_pk = 1
        login = self.client.login(username="Test", password="test")
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
        login = self.client.login(username="Test", password="test")
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
        # print(SeasonStage.objects.all().count())
        # t = SeasonStage.objects.get(id=3).teamseason_set.all()
        # print(t)
        resp = self.client.post(reverse("league-admin-season-stage-create",
            kwargs={"season_year": season_year, "season_pk": season_pk}),
            stage_data,
            follow=True
            )

        # print(SeasonStage.objects.all().count())
        # print(SeasonStage.objects.get(id=4))
        # t = SeasonStage.objects.get(id=4).teamseason_set.all()
        # print(t)
        print("ToDo: Figure how to pass data to formsets")
        self.assertRedirects(resp, reverse("league-admin-season-stage",
            kwargs={"season_year": season_year, "season_pk": season_pk}))



