from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, SeasonStage, TeamSeason
from stats.models import TeamGameLineScore, TeamGameStats



class TeamGameLinescoreCreateViewTest(TestCase):
    """
    Tests team_game_linescore_create_view
    from stats/views/tg_linescore_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/linescore/
        <int:team_game_stats_pk>',
    views.team_game_linescore_create_view,
    name='stats-linescore-create'

    View does NOT exist as a page
    -->Redirect to stats-team-game-stats
    -->or team_game_stats_info_view
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=1)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )


    def test_view_without_logging_in(self):
        response = self.client.get('/league/stats/game/2/team/1/linescore/1')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/stats/game/2/team/1/linescore/1')
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk
            }))
        self.assertEqual(response.status_code, 302)


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk
            }))
        self.assertRedirects(response, reverse("stats-team-game-stats", 
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))



class TeamGameLinescoreEditViewTest(TestCase):
    """
    Tests team_game_linescore_edit_view
    from stats/views/tg_linescore_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/linescore/
        <int:team_game_stats_pk>/<int:linescore_pk>/edit',
    views.team_game_linescore_edit_view,
    name='stats-linescore-edit'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=1)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

        cls.tgls = TeamGameLineScore.objects.create(
            game=cls.tgs
        )


    def test_view_without_logging_in(self):
        url = (
            f'/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/'
            f'linescore/{self.tgs.pk}/{self.tgls.pk}/edit'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f'/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/'
            f'linescore/{self.tgs.pk}/{self.tgls.pk}/edit'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"stats/game_linescore_create.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game_pk"], self.game.pk)
        self.assertEqual(response.context["team_season_pk"],
            self.team_season.pk)
        self.assertEqual(response.context["game_stats"], self.tgs)
        self.assertEqual(response.context["linescore"], self.tgls)
        self.assertTrue(response.context["form"] is not None)

    
    def test_edit(self):
        data= {
            "first":4,
            "second":0,
        }
        self.client.login(username="Test", password="test")
        self.client.post(reverse('stats-linescore-edit',
                kwargs={
                    "game_pk": self.game.pk,
                    "team_season_pk": self.team_season.pk,
                    "team_game_stats_pk": self.tgs.pk,
                    "linescore_pk": self.tgls.pk
                }),
            data=data,
            follow=True
        )
        tgls = TeamGameLineScore.objects.get(pk=self.tgls.pk)
        self.assertTrue(self.tgls.first != tgls.first)
        self.assertEqual(tgls.first, 4)

    
    def test_redirects(self):
        data= {
            "first":4,
            "second":0,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-linescore-edit',
                kwargs={
                    "game_pk": self.game.pk,
                    "team_season_pk": self.team_season.pk,
                    "team_game_stats_pk": self.tgs.pk,
                    "linescore_pk": self.tgls.pk
                }),
            data=data,
            follow=True
        )
        self.assertRedirects(response, reverse("stats-team-game-stats",
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))

    def test_does_not_exist(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-edit',
                kwargs={
                    "game_pk": self.game.pk,
                    "team_season_pk": 9,
                    "team_game_stats_pk": self.tgs.pk,
                    "linescore_pk": 9
                }),
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game_pk"], self.game.pk)
        self.assertEqual(response.context["team_season_pk"],9)
        self.assertEqual(response.context["game_stats"], self.tgs)
        self.assertEqual(response.context["linescore"], None)
        self.assertTrue(response.context["form"] is not None)




class TeamGameLinescoreDeleteViewTest(TestCase):
    """
    Tests team_game_linescore_delete_view
    from stats/views/tg_linescore_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/linescore/
        <int:team_game_stats_pk>/<int:linescore_pk>/delete',
    views.team_game_linescore_delete_info_view,
    name='stats-linescore-delete'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=1)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

        cls.tgls = TeamGameLineScore.objects.create(
            game=cls.tgs
        )

    def test_view_without_logging_in(self):
        url = (
            f'/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/'
            f'linescore/{self.tgs.pk}/{self.tgls.pk}/delete'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f'/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/'
            f'linescore/{self.tgs.pk}/{self.tgls.pk}/delete'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"stats/game_linescore_delete.html")

    
    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-linescore-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game_pk"], self.game.pk)
        self.assertEqual(response.context["team_season_pk"],
            self.team_season.pk)
        self.assertEqual(response.context["linescore"], self.tgls)
        self.assertTrue(response.context["nested_object"] is not None)


    def test_delete(self):
        count = TeamGameLineScore.objects.filter(game=self.tgs).count()
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-linescore-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }), follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{self.tgls} and all related objects were deleted.')

        count2 = TeamGameLineScore.objects.filter(game=self.tgs).count()
        self.assertEqual(count-1, count2)


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-linescore-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
                "linescore_pk": self.tgls.pk
            }))
        self.assertRedirects(response, reverse("stats-team-game-stats",
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))


