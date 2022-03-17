from django.test import TestCase
from django.urls import reverse

from league.models import League, Player
# from league_admin.forms import PlayerCreateForm


class LAPlayerCreateView(TestCase):
    """
    Test league_admin_player_create_view from league_admin/views/player_views.py
    
    'players/add',
    views.league_admin_player_create_view,
    name='league-admin-player-create'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/players/add')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/add')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_create.html")


    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        self.assertEqual(response.context["league"], league)
        self.assertTrue(response.context["form"] is not None)


class LAPlayerSelectViewTest(TestCase):
    """
    Test league_admin_player_select_view from league_admin/views/player_views.py
    
    'players/',
    views.league_admin_player_select_view,
    name='league-admin-player-select'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        for i in range(28):
            player = Player.objects.create(
                league=cls.league,
                first_name="Firsty",
                last_name="McFirsterson")


    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/players/')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/')
        self.assertEqual(response.status_code, 200)
    

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_select.html")

    
    def test_pagination_is_ten(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)
        # self.assertTrue("is_paginated" in response.context)
        # self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(response.context["paginator"] is not None)
        self.assertEqual(len(response.context['all_players']), 25)


    def test_pagination_page_2(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select")+"?page=2")
        self.assertEqual(response.status_code, 200)
        # self.assertTrue("paginator" in response.context)
        # self.assertTrue(response.context["paginator"] == True)
        #Initially created 2 players, 3 + 2 left for 2nd page
        self.assertTrue(response.context["paginator"] is not None)
        self.assertEqual(len(response.context['all_players']), 5)

    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)
        

        league = League.objects.get(id=1)
        self.assertEqual(response.context["league"], league)
        self.assertTrue(response.context["filter"] is not None)
        self.assertTrue(response.context["paginator"] is not None)
