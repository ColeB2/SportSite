import datetime
from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, Season, SeasonStage, TeamSeason
from league_admin.forms import EditGameForm

class LAEditGameViewTest(TestCase):
    """
    Tests league_admin_edit_game_view from league_admin/views/game_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>/<game_pk>/edit'
    'league-admin-game-edit'
    views.league_admin_edit_game_view
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/1/1/edit')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/1/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 3, "game_pk":1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 3, "game_pk":1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "league_admin/game_templates/game_edit.html")

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 3, "game_pk":1}))
        self.assertEqual(response.status_code, 200)

        game = Game.objects.get(id=1)
        self.assertEqual(response.context["game_instance"], game)
        self.assertEqual(response.context["season_year"], 2022)
        self.assertEqual(response.context["season_stage_pk"], 3)
        self.assertTrue(response.context["form"] is not None)
        #More Form Tests context?

    def test_game_edit(self):
        """Current Ssetup un testable? --> Works for use, not for automated
        testing"""
        """
        game_data = {"year": 2022, "season_stage_pk": 3, "game_pk": 1}
        game = Game.objects.get(pk=game_data["game_pk"])

        # post = {"home_team": game.home_team, "away_team":game.away_team,
        #     "location": game.location, 
        #     "date_year": game.date.year, "date_month": game.date.month,
        #     "date_day": game.date.day,
        #     "start_time": game.start_time, 
        #     "home_score":9, "away_score": 3}
        t1 = TeamSeason.objects.get(id="1")
        t2 = TeamSeason.objects.get(id="2")
        time = datetime.time(17, 00, 00)

        date = datetime.datetime(2022, 5,18)
        # post = {"home_team": t1, "away_team":t2,
        #     "location": game.location, 
        #     "date": date,
        #     "start_time": game.start_time, 
        #     "home_score":9, "away_score": 3}

        post = {"home_team": t1, "away_team": t2, "date_year": date.year,
            "date_month": date.month, "date_day": date.day,
            "start_time": time, "home_score": 99, "away_score": 0}


        self.client.login(username="Test", password="test")
        # response = self.client.post(reverse(
        #     'league-admin-game-edit',
        #     kwargs={
        #         "season_year": game_data["year"], 
        #         "season_stage_pk": game_data["season_stage_pk"], 
        #         "game_pk": game_data["game_pk"]}),
        #     post,
        #     follow=True)

        response = self.client.post(reverse('league-admin-game-edit',
            kwargs={
                "season_year": 2022,
                "season_stage_pk": 3,
                "game_pk":1}),
                post, follow=True)
        print(response.context["stage"])
        game1, game2 = Game.objects.all()
        print(game1.home_score, game2.home_score)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{game} changed.')

        game = Game.objects.get(pk=1)
        print(game.home_score)
        print(Game.objects.all())
        """


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 3, "game_pk":1}))
        self.assertEqual(response.status_code, 200)

        post = {"home_score":10, "away_score": 0}

        response = self.client.post(reverse(
            'league-admin-game-edit',
            kwargs={"season_year": 2022, "season_stage_pk": 3, "game_pk":1}),
            post,
            follow=True)


        self.assertRedirects(response, reverse("league-admin-schedule",
            kwargs={"season_year": 2022, "season_stage_pk": 3}))



class LADeleteGameInfoViewTest(TestCase):
    """
    Tests league_admin_delete_game_info_view from league_admin/views/game_views.py

    'schedule/<int:season_year>/stages/<season_stage_pk>/<game_pk>/delete'
    'league-admin-game-delete'
    views.league_admin_delete_game_info_view
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=1)
        cls.home = TeamSeason.objects.get(id=1)
        cls.away = TeamSeason.objects.get(id=2)
        gdate = datetime.date(2022, 3, 15)
        cls.game = Game.objects.create(season=cls.stage, home_team=cls.home, away_team=cls.away, date=gdate)

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/schedule/2022/stages/1/1/delete')
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/schedule/2022/stages/1/1/delete')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-delete',
            kwargs={"season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk, "game_pk": self.game.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-delete',
            kwargs={"season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk, "game_pk": self.game.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "league_admin/game_templates/game_delete.html")

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-game-delete',
            kwargs={"season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk, "game_pk": self.game.pk}))
        self.assertEqual(response.status_code, 200)

        # game = Game.objects.get(id=1)
        self.assertEqual(response.context["game"], self.game)
        self.assertEqual(response.context["season_year"], int(self.stage.season.year))
        self.assertEqual(response.context["season_stage_pk"], self.stage.pk)
        self.assertTrue(response.context["nested_object"] is not None)
        #More nested_obj Tests?

    def test_delete(self):
        games_count = Game.objects.filter(season=self.stage).count()

        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('league-admin-game-delete',
            kwargs={"season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk, "game_pk": self.game.pk}),
            follow=True)
        self.assertEqual(response.status_code, 200)


        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{self.game} and all related objects were deleted.')

        games_count_del = Game.objects.filter(season=self.stage).count()

        self.assertEqual(games_count-1, games_count_del)


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('league-admin-game-delete',
            kwargs={"season_year": self.stage.season.year,
                    "season_stage_pk": self.stage.pk, "game_pk": self.game.pk}),
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertRedirects(response, reverse("league-admin-schedule", 
            kwargs={
                "season_year": self.game.date.year,
                "season_stage_pk": self.stage.pk}))

