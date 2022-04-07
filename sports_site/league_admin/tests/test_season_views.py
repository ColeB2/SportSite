from django.test import TestCase
from django.urls import reverse

from league.models import League, Season


class LASeasonViewTest(TestCase):
    """
    Tests league_admin_season_view
        from league_admin/views/season_views.py

    'season/',
    views.league_admin_season_view,
    name='league-admin-season')
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/')
        self.assertEqual(response.status_code, 302)
        

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_templates/season_page.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league)

        self.assertQuerysetEqual(
            response.context["seasons"], seasons, ordered=False)


class LACreateSeasonViewTest(TestCase):
    """
    Tests league_admin_create_season_view
        from league_admin/views/season_views.py

    'season/add/new',
    views.league_admin_create_season_view,
    name='league-admin-season-create',
    """
    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/season/add/new')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/season/add/new')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_templates/season_create.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league)

        self.assertQuerysetEqual(
            response.context["seasons"], seasons, ordered=False)
        self.assertTrue(response.context["form"] is not None)

    
    def test_create_seasons(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league).count()

        data = {"year": 3000}


        response = self.client.post(reverse("league-admin-season-create"),
            data, follow=True)

        self.assertRedirects(response, reverse("league-admin-season"))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'{data["year"]} created.')

        seasons2 = Season.objects.filter(league=league).count()
        self.assertTrue(seasons2 -1 == seasons)

    
    def test_creates_objects_already_exists(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-create"))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        Season.objects.create(league=league, year="3000")
        seasons = Season.objects.filter(league=league).count()
        

        data = {"year": 3000}


        response = self.client.post(reverse("league-admin-season-create"),
            data, follow=True)

        self.assertRedirects(response, reverse("league-admin-season"))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'{data["year"]} already exists.')

        seasons2 = Season.objects.filter(league=league).count()
        self.assertTrue(seasons2 == seasons)



class LASeasonDeleteInfoViewTest(TestCase):
    """
    Tests league_admin_season_delete_info_view
        from league_admin/views/season_views.py

    'season/<int:season_year>/<season_pk>/delete',
    views.league_admin_season_delete_info_view,
    name='league-admin-season-delete'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.season = Season.objects.create(league=cls.league, year="2030")


    def test_view_without_logging_in(self):
        response = self.client.get(
            f'/league/admin/season/{self.season.year}/{self.season.pk}/delete')
        self.assertEqual(response.status_code, 302)

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(
            f'/league/admin/season/{self.season.year}/{self.season.pk}/delete')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-delete",
            kwargs={"season_year": self.season.year,
                    "season_pk": self.season.pk}))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-delete",
            kwargs={"season_year": self.season.year,
                    "season_pk": self.season.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_templates/season_delete.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-delete",
            kwargs={"season_year": self.season.year,
                    "season_pk": self.season.pk}))
        self.assertEqual(response.status_code, 200)

        season = Season.objects.get(pk=self.season.pk)

        self.assertEqual(season, self.season)
        self.assertTrue(response.context["nested_object"] is not None)

    
    def test_deletes_seasons(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-delete",
            kwargs={"season_year": self.season.year,
                    "season_pk": self.season.pk}))
        self.assertEqual(response.status_code, 200)

        league = League.objects.get(id=1)
        seasons = Season.objects.filter(league=league).count()

        response = self.client.post(reverse("league-admin-season-delete",
            kwargs={"season_year": self.season.year,
                    "season_pk": self.season.pk}), 
            follow=True)

        self.assertRedirects(response, reverse("league-admin-season"))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
            f'{self.season} and all related objects were deleted.')

        seasons2 = Season.objects.filter(league=league).count()
        self.assertTrue(seasons2 + 1  == seasons)


class LASeasonEditViewTest(TestCase):
    """
    Tests SeasonEditView
        from league_admin/views/season_views.py

    'season/<int:season_year>/<season_pk>/<int:pk>/edit/season',
    SeasonEditView.as_view(),
    name='league-admin-season-edit'
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.season = Season.objects.create(league=cls.league, year="2030")


    def test_view_without_logging_in(self):
        response = self.client.get(
            f'/league/admin/season/'
            + f'{self.season.year}/{self.season.pk}/{self.season.pk}'
            + f'/edit/season')
        self.assertEqual(response.status_code, 403)
        

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(
            f'/league/admin/season/'
            + f'{self.season.year}/{self.season.pk}/{self.season.pk}'
            + f'/edit/season')
        self.assertEqual(response.status_code, 200)

    
    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-edit",
            kwargs={
                "season_year":self.season.year,
                "season_pk": self.season.pk,
                "pk":self.season.pk}))
        self.assertEqual(response.status_code, 200)
        

    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-edit",
            kwargs={
                "season_year":self.season.year,
                "season_pk": self.season.pk,
                "pk":self.season.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/season_templates/season_edit.html")

    
    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-edit",
            kwargs={
                "season_year":self.season.year,
                "season_pk": self.season.pk,
                "pk":self.season.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context["form"] is not None)
        self.assertEqual(response.context["season"], self.season)

    
    def test_edit_season(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-season-edit",
            kwargs={
                "season_year":self.season.year,
                "season_pk": self.season.pk,
                "pk":self.season.pk}))
        self.assertEqual(response.status_code, 200)

        year = "2050"
        data = {"year": year}

        response = self.client.post(reverse("league-admin-season-edit",
            kwargs={
                "season_year":self.season.year,
                "season_pk": self.season.pk,
                "pk":self.season.pk}),
                data,
                follow=True)

        self.assertRedirects(response, reverse("league-admin-season-stage",
            args=[year, self.season.pk]))

        season = Season.objects.get(pk=self.season.pk)
        self.assertTrue(season.year != self.season.year)
        self.assertEqual(season.year, year)
