from django.test import TestCase
from django.urls import reverse

from league.models import (Game, League, Player, PlayerSeason, Roster,
    SeasonStage, TeamSeason)
from stats.models import PlayerHittingGameStats, TeamGameStats


class TeamGameStatsCreateViewTest(TestCase):
    """
    Tests team_game_stats_create_view
    from stats/views/tgs_hitting_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/lineup/
        <int:team_game_stats_pk>/create',
    views.team_game_stats_create_view,
    name='stats-game-stats-create'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)
        cls.roster = Roster.objects.get(team=cls.team_season)
        cls.players = cls.roster.playerseason_set.all()

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

    def test_view_without_logging_in(self):
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"lineup/{self.tgs.pk}/create"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"lineup/{self.tgs.pk}/create"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "stats/game_stats_create.html")
    

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game"], self.game)
        self.assertEqual(response.context["team_season"],self.team_season)
        
        self.assertEqual(response.context["roster"], self.roster)
        
        self.assertQuerysetEqual(
            response.context["players"], self.players, ordered=False)
        self.assertTrue(response.context["formset"] is not None)

    
    def test_create(self):
        count = PlayerHittingGameStats.objects.all().count()
        data= {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": len(self.players),
            "form-MAX_NUM_FORMS": "",

            #form 0
            "form-0-player": self.players[0].id,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)
        
        count2 = PlayerHittingGameStats.objects.all().count()
        phgs = PlayerHittingGameStats.objects.get(id=3)
        self.assertTrue(count+1 == count2)
        self.assertEqual(phgs.player, self.players[0])
        self.assertEqual(phgs.season, self.stage)
        self.assertEqual(phgs.team_stats, self.tgs)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{phgs.player.player} hitting stats created for {self.game}.')

    def test_create_different_slot_post_twice(self):
        player = Player.objects.create(
            league=self.league,
            first_name="Throwaway",
            last_name="Player")
        player_season = PlayerSeason.objects.create(
            player=player, team=self.roster, season=self.stage,
            number=00, position="LF")
        
        players = self.roster.playerseason_set.all()
        count = PlayerHittingGameStats.objects.all().count()
        data= {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": len(self.players),
            "form-MAX_NUM_FORMS": "",

            #form 0
            "form-1-player": self.players[0].id,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)

        response = self.client.post(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)
        
        count2 = PlayerHittingGameStats.objects.all().count()
        phgs = PlayerHittingGameStats.objects.get(id=3)
        self.assertTrue(count+1 == count2)
        self.assertEqual(phgs.player, self.players[0])
        self.assertEqual(phgs.season, self.stage)
        self.assertEqual(phgs.team_stats, self.tgs)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{phgs.player.player} already has stats for {self.game}.')

    
    def test_redirects(self):
        data= {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": len(self.players),
            "form-MAX_NUM_FORMS": "",

            #form 0
            "form-0-player": self.players[0].id,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)

        self.assertRedirects(response, reverse("stats-team-game-stats",
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))

    def test_create_already_exists(self):
        data= {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": len(self.players),
            "form-MAX_NUM_FORMS": "",

            #form 0
            "form-0-player": self.players[0].id,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)
        response = self.client.post(reverse('stats-game-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)
        
        phgs = PlayerHittingGameStats.objects.get(id=3)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{phgs.player.player} already has stats for {self.game}.')


class TeamGameStatsEditViewTest(TestCase):
    """
    Tests team_game_stats_edit_view
    from stats/views/tgs_hitting_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/lineup/
        <int:team_game_stats_pk>/edit',
    views.team_game_stats_edit_view,
    name='stats-game-stats-edit'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)
        cls.roster = Roster.objects.get(team=cls.team_season)
        cls.players = cls.roster.playerseason_set.all()

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )


    def test_view_without_logging_in(self):
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"lineup/{self.tgs.pk}/edit"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"lineup/{self.tgs.pk}/edit"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "stats/game_stats_edit.html")
    

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game"], self.game)
        self.assertEqual(response.context["team_season"],self.team_season)
        
        self.assertEqual(response.context["roster"], self.roster)
        
        self.assertQuerysetEqual(
            response.context["players"], self.players, ordered=False)
        self.assertTrue(response.context["formset"] is not None)
        self.assertTrue(response.context["helper"] is not None)

    def test_edit(self):
        data= {
            "playerhittinggamestats_set-INITIAL_FORMS": 0,
            "playerhittinggamestats_set-TOTAL_FORMS": len(self.players),
            "playerhittinggamestats_set-MAX_NUM_FORMS": "",

            #form 0
            "playerhittinggamestats_set-0-player": self.players[0].id,
            "playerhittinggamestats_set-0-at_bats": 100,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)
        
        player = self.players[0]
        phgs = player.playerhittinggamestats_set.get(team_stats=self.tgs)

        self.assertEqual(phgs.player, self.players[0])
        self.assertEqual(phgs.season, self.stage)
        self.assertEqual(phgs.team_stats, self.tgs)
        self.assertEqual(phgs.at_bats, 100)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{phgs} saved.')


    def test_redirects(self):
        data= {
            "playerhittinggamestats_set-INITIAL_FORMS": 0,
            "playerhittinggamestats_set-TOTAL_FORMS": len(self.players),
            "playerhittinggamestats_set-MAX_NUM_FORMS": "",

            #form 0
            "playerhittinggamestats_set-0-player": self.players[0].id,
            "playerhittinggamestats_set-0-at_bats": 100,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-edit',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)
        
        self.assertRedirects(response, reverse("stats-team-game-stats",
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))


class TeamGameStatsDeleteInfoViewTest(TestCase):
    """
    Tests team_game_stats_delete_info_view
    from stats/views/tgs_hitting_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/lineup/
        <int:team_game_stats_pk>/delete,',
    views.team_game_stats_delete_info_view,
    name='stats-game-stats-delete'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.stage = SeasonStage.objects.get(id=3)
        cls.team_season = TeamSeason.objects.get(id=1)
        cls.game = Game.objects.get(id=2)
        cls.roster = Roster.objects.get(team=cls.team_season)
        cls.players = cls.roster.playerseason_set.all()

        cls.tgs = TeamGameStats.objects.create(
            season=cls.stage,
            team=cls.team_season,
            game=cls.game
        )

        cls.phgs = PlayerHittingGameStats.objects.create(
            team_stats=cls.tgs,
            season=cls.stage,
            player=cls.players[0]
        )

    def test_view_without_logging_in(self):
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"lineup/{self.tgs.pk}/delete"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"lineup/{self.tgs.pk}/delete"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "stats/game_stats_delete.html")
    

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-stats-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["game_pk"], self.game.pk)
        self.assertEqual(response.context["team_season_pk"],self.team_season.pk)
        self.assertEqual(response.context["game_stats"], self.tgs)
        
        self.assertQuerysetEqual(
            response.context["hitting_stats"],
            self.tgs.playerhittinggamestats_set.all(),
            ordered=False)

    def test_delete(self):
        count = PlayerHittingGameStats.objects.all().count()
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{self.phgs} and all related objects were deleted.')
        
        
        count2 = PlayerHittingGameStats.objects.all().count()
        self.assertEqual(count - 1, count2)


    def test_redirects(self):
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-stats-delete',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            follow=True)

        self.assertRedirects(response, reverse("stats-team-game-stats",
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk
            }))



