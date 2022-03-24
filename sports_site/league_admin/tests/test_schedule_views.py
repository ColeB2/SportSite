from datetime import datetime
from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, SeasonStage, TeamSeason


class LAScheduleSelectViewTest(TestCase):
    """
    Tests league_admin_schedule_select_view
        from league_admin/views/schedule_views.py

    'schedule/',
    views.league_admin_schedule_select_view,
    name='league-admin-schedule-select'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_select.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)

        stages = SeasonStage.objects.filter(
            season__league=League.objects.get(id=1))
        self.assertQuerysetEqual(
            response.context["stages"], stages, ordered=False)



class LAScheduleViewTest(TestCase):
    """
    Tests league_admin_schedule_view
        from league_admin/views/schedule_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>',
    views.league_admin_schedule_view,
    name='league-admin-schedule'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/1')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_view.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=3)
        schedule = Game.objects.filter(season__pk="3")

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"],"3")
        self.assertEqual(response.context["stage"],stage)
        self.assertQuerysetEqual(
            response.context["schedule"],
            schedule,
            ordered=False)


class LAScheduleCreateViewTest(TestCase):
    """
    Tests league_admin_schedule_create_view
        from league_admin/views/schedule_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>/create',
    views.league_admin_schedule_create_view,
    name='league-admin-schedule-create'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/3/create')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3/create')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_create.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=3)
        schedule = Game.objects.filter(season__pk="3")

        self.assertTrue(response.context["formset"] is not None)
        self.assertEqual(response.context["current_stage"], stage)


    def test_success_url(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)

        resp = self.client.post(reverse(
                "league-admin-schedule-create",
                kwargs={"season_year": 2022, "season_stage_pk": "3"}),
            {},
            follow=True,
            extra={"create":"create"})
        self.assertEqual(resp.status_code,200)
        # print(resp)
        # self.assertRedirects(resp, reverse(
        #     "league-admin-schedule",
        #     kwargs={"season_year": 2022, "season_stage_pk": "3"})
        # )
        ##ToDo Figure out success url redirects.


class LAScheduleDeleteInfoViewTest(TestCase):
    """
    Tests league_admin_schedule_delete_info_view
        from league_admin/views/schedule_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>/delete',
    views.league_admin_schedule_delete_info_view,
    name='league-admin-schedule-delete-info')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/3/delete')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3/delete')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_delete.html")

    
    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=3)
        schedule = Game.objects.filter(season__pk="3")
        games = stage.game_set.all()

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"],"3")
        self.assertEqual(response.context["stage"],stage)
        self.assertQuerysetEqual(
            response.context["games"],
            games,
            ordered=False)
        self.assertTrue(response.context["nested_games"] is not None)


    def test_delete(self):
        self.assertTrue(Game.objects.all().count() != 0)
        login = self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}), follow=True)
        self.assertRedirects(response,
            reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": "3"}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all().count() == 0)

    def test_post_delete(self):
        self.assertTrue(Game.objects.all().count() != 0)

