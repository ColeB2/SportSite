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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/add')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_create.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        self.assertEqual(response.context["league"], league)
        self.assertTrue(response.context["form"] is not None)

    def test_create_player(self):
        first = "Firsty"
        last = "McLasty"
        post = {"first_name": first, "last_name": last}
        league = League.objects.get(id=1)
        player_len1 = Player.objects.filter(league=league).count()

        self.client.login(username="Test", password="test")
        self.client.post(reverse("league-admin-player-create"),
            data=post,
            follow=True)

        player_len2 = Player.objects.filter(league=league).count()
        self.assertEqual(player_len2-1, player_len1)

        player = Player.objects.get(first_name="Firsty")
        self.assertEqual(player.first_name, first)
        self.assertEqual(player.last_name, last)

    
    def test_redirects(self):
        post = {"first_name": "Firsty", "last_name": "McLasty"}
        
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse("league-admin-player-create"),
            data=post,
            follow=True)

        self.assertRedirects(response, reverse("league-admin-dashboard"))



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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/')
        self.assertEqual(response.status_code, 200)
    

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_select.html")

    
    def test_pagination_is_ten(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)
        # self.assertTrue("is_paginated" in response.context)
        # self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(response.context["paginator"] is not None)
        context_len = len(response.context["all_players"])
        self.assertEqual(context_len, 25)


    def test_pagination_page_2(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select")+"?page=2")
        self.assertEqual(response.status_code, 200)
        # self.assertTrue("paginator" in response.context)
        # self.assertTrue(response.context["paginator"] == True)
        #Initially created 2 players, 3 + 2 left for 2nd page
        self.assertTrue(response.context["paginator"] is not None)
        self.assertEqual(len(response.context['all_players']), 5)

    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-select"))
        self.assertEqual(response.status_code, 200)
        

        league = League.objects.get(id=1)
        self.assertEqual(response.context["league"], league)
        self.assertTrue(response.context["filter"] is not None)
        self.assertTrue(response.context["paginator"] is not None)
        self.assertTrue(response.context["all_players"] is not None)


class LAPlayerEditViewTest(TestCase):
    """
    Test league_admin_player_edit_view from league_admin/views/player_views.py
    
    'players/<int:player_pk>/edit',
    views.league_admin_player_edit_view,
    name='league-admin-player-edit')
    """
    @classmethod
    def setUpTestData(cls) -> None:
        cls.league = League.objects.get(id = 1)
        cls.player = Player.objects.create(
            league=cls.league,
            first_name="Last",
            last_name="Lasty")
        
        return super().setUpTestData()
    
    
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/players/1/edit')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/1/edit')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-edit",
            kwargs={"player_pk": self.player.pk}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-edit",
            kwargs={"player_pk": self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_edit.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-edit",
            kwargs={"player_pk": self.player.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context["form"] is not None)
        self.assertTrue(response.context["player_instance"].pk == self.player.pk)


    def test_edit_player(self):
        post = {"first_name": "Last", "last_name": "McLasterson"}

        self.client.login(username="Test", password="test")
        self.client.post(reverse("league-admin-player-edit",
            kwargs={"player_pk": self.player.pk}),
            post,
            follow=True)

        edited_player = Player.objects.get(pk=self.player.pk)
        self.assertTrue(edited_player.first_name == "Last")
        self.assertTrue(edited_player.last_name == "McLasterson")



    def test_redirect(self):
        self.client.login(username="Test", password="test")
        post = {"first_name": "Last", "last_name": "McLasterson"}
        resp = self.client.post(reverse("league-admin-player-edit",
            kwargs={"player_pk": self.player.pk} ),
            post,
            follow=True)

        self.assertRedirects(resp, reverse("league-admin-player-select"))


class LAPlayerDeleteInfoViewTest(TestCase):
    """
    Test league_admin_player_delete_info_view from
        league_admin/views/player_views.py
    
    'players/<player_pk>/delete',
    views.league_admin_player_delete_info_view,
    name='league-admin-player-delete'
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/players/1/delete')
        self.assertEqual(response.status_code, 302)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/players/1/delete')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-delete",
            kwargs={"player_pk": 1}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-delete",
            kwargs={"player_pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/player_templates/player_delete.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-delete",
            kwargs={"player_pk": 1}))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context["nested_object"] is not None)
        self.assertTrue(response.context["player"].pk == 1)


    def test_player_delete(self):
        l = League.objects.get(id=1)
        player = Player.objects.create(
            league= l, first_name="Last",last_name="Lasty")

        len_player = len(Player.objects.all())
        

        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-player-delete",
            kwargs={"player_pk": player.pk}))
        self.assertEqual(response.status_code, 200)

        resp = self.client.post(reverse("league-admin-player-delete",
            kwargs={"player_pk": player.pk}), follow=True)

        self.assertEqual(resp.status_code, 200)
        len_player2 = len(Player.objects.all())
        self.assertTrue(len_player - len_player2 == 1)



