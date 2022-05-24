from django.test import TestCase
from django.urls import reverse

from league.models import Game, League, Roster, SeasonStage, TeamSeason
from stats.models import PlayerPitchingGameStats, TeamGameStats


class TeamGamePitchingStatsCreateViewTest(TestCase):
    """
    Tests team_game_pitching_stats_create_view
    from stats/views/tgs_pitching_views.py

    'game/<int:game_pk>/team/<int:team_season_pk>/pitching/
        <int:team_game_stats_pk>/create',
    views.team_game_pitching_stats_create_view,
    name='stats-game-pitching-stats-create'
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
            f"pitching/{self.tgs.pk}/create"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        url = (
            f"/league/stats/game/{self.game.pk}/team/{self.team_season.pk}/" +
            f"pitching/{self.tgs.pk}/create"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-pitching-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-pitching-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "stats/game_pitching_stats_create.html")
    

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('stats-game-pitching-stats-create',
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
        count = PlayerPitchingGameStats.objects.all().count()
        print(count)
        print(self.tgs)
        data= {
            "create": True,
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": len(self.players),
            "form-MAX_NUM_FORMS": "",
            #form 0
            "form-0-player": self.players[0].id,
        }
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse('stats-game-pitching-stats-create',
            kwargs={
                "game_pk": self.game.pk,
                "team_season_pk": self.team_season.pk,
                "team_game_stats_pk": self.tgs.pk,
            }),
            data=data,
            follow=True)

        print(data)
        
        count2 = PlayerPitchingGameStats.objects.all().count()
        print(count2)
        ppgs = PlayerPitchingGameStats.objects.get(id=count2)
        print(ppgs)
        self.assertTrue(count+1 == count2)
        self.assertEqual(ppgs.player, self.players[0])
        self.assertEqual(ppgs.season, self.stage)
        self.assertEqual(ppgs.team_stats, self.tgs)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{ppgs.player.player} pitching stats created for {self.game}.')