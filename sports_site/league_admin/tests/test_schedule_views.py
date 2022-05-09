import datetime
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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-schedule-select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_select.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_view.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=3)
        schedule = Game.objects.filter(season__pk=3)

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"], 3)
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
    @classmethod
    def setUpTestData(cls) -> None:
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=3)
        cls.t1 = TeamSeason.objects.get(id=1)
        cls.t2 = TeamSeason.objects.get(id=2)
        return super().setUpTestData()

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/3/create')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3/create')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_create.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-create",
            kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}))
        self.assertEqual(response.status_code, 200)


        self.assertTrue(response.context["formset"] is not None)
        self.assertEqual(response.context["current_stage"], self.stage)


    def test_create_games(self):
        date = datetime.date(2022, 3, 11)
        time = datetime.time(18, 30)
        data = {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": 5,
            "form-MAX_NUM_FORMS": "",

            #form 1
            "form-0-home_team": self.t2.id,
            "form-0-away_team": self.t1.id,
            "form-0-date": date,
            "form-0-start_time": time,
            "form-0-location": self.t2.team.place
        }
        game_len = Game.objects.all().count()
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
                "league-admin-schedule-create",
                kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}),
            data=data,
            follow=True)
 
        game_len_2 = Game.objects.all().count()
        self.assertEqual(game_len+1, game_len_2)
        # print(Game.objects.get(date=date))
        game = Game.objects.get(date=date)
        self.assertEqual(game.home_team, self.t2)
        self.assertEqual(game.away_team, self.t1)
        self.assertEqual(game.date, date)


    def test_redirects(self):
        data = {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": 5,
            "form-MAX_NUM_FORMS": "",
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
                "league-admin-schedule-create",
                kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}),
            data=data,
            follow=True)
 
        self.assertRedirects(response, reverse(
            "league-admin-schedule",
            kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk})
        )

    def test_create_and_continue_redirects(self):
        data = {
            "create-and-continue": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": 5,
            "form-MAX_NUM_FORMS": "",
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
                "league-admin-schedule-create",
                kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}),
            data=data,
            follow=True)
 
        self.assertRedirects(response, reverse(
            "league-admin-schedule-create",
            kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk})
        )

    def test_create_and_continue_creates(self):
        date = datetime.date(2022, 5, 11)
        data = {
            "create-and-continue": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": 5,
            "form-MAX_NUM_FORMS": "",

            #form 1
            "form-0-home_team": self.t2.id,
            "form-0-away_team": self.t1.id,
            "form-0-date": date
        }
        game_len = Game.objects.all().count()
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
                "league-admin-schedule-create",
                kwargs={
                    "season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk}),
            data=data,
            follow=True)
 
        game_len_2 = Game.objects.all().count()
        self.assertEqual(game_len+1, game_len_2)

        game = Game.objects.get(date=date)
        self.assertEqual(game.home_team, self.t2)
        self.assertEqual(game.away_team, self.t1)
        self.assertEqual(game.date, date)


    


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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/3/delete')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/schedule_templates/schedule_delete.html")

    
    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)

        stage = SeasonStage.objects.get(pk=3)
        schedule = Game.objects.filter(season__pk=3)
        games = stage.game_set.all()

        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"],3)
        self.assertEqual(response.context["stage"],stage)
        self.assertQuerysetEqual(
            response.context["games"],
            games,
            ordered=False)
        self.assertTrue(response.context["nested_games"] is not None)


    def test_delete(self):
        self.assertTrue(Game.objects.all().count() != 0)
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
            "league-admin-schedule-delete-info",
            kwargs={"season_year": 2022, "season_stage_pk": 3}), follow=True)
        self.assertRedirects(response,
            reverse(
            "league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Game.objects.all().count() == 0)

    def test_post_delete(self):
        self.assertTrue(Game.objects.all().count() != 0)

