from django.test import TestCase
from django.urls import reverse

from league.models import League, Roster, TeamSeason
from news.models import Article
from ..filters import RosterFilter, ArticleFilter

class LADashboardViewTest(TestCase):
    """
    Tests league_admin_dashboard_view from league_admin/views/views.py
    """

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league_admin/dashboard.html')

    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        # Len of empty context --> 2
        self.assertEqual(len(response.context), 2)


class LARosterSelectTest(TestCase):
    """
    Tests league_admin_roster_select from league_admin/views/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.teamseason = TeamSeason.objects.all()[0]
        for i in range(13):
            roster = Roster.objects.create(team=cls.teamseason)

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/roster/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/roster/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-roster-select'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-roster-select'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league_admin/roster_select.html')

    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-roster-select'))
        self.assertEqual(response.status_code, 200)
        # Len of empty context --> 2
        self.assertEqual(len(response.context), 18)
        print(response.context["filter"])
        print(response.context["paginator"])
        print(response.context["all_rosters"])
        self.assertTrue(response.context["filter"] is not None)
        self.assertTrue(response.context["paginator"] is not None)
        self.assertTrue(response.context["all_rosters"] is not None)
        # self.assertEqual(response.context["filter"], ArticleFilter)


    def test_pagination_is_ten(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-roster-select'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("paginator" in response.context)
        # self.assertTrue(response.context["paginator"] == True)
        self.assertEqual(len(response.context['paginator'].page(1)), 10)

    def test_pagination_page_2(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-roster-select')+"?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("paginator" in response.context)
        # self.assertTrue(response.context["is_paginated"] == True)
        #2 Original rosters plus 13 create --> 15, 10 and 5
        self.assertEqual(len(response.context['paginator'].page(2)), 5)


class LANewsSelectTest(TestCase):
    """
    Tests league_admin_news_select from league_admin/views/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        for i in range(13):
            article = Article.objects.create(league=cls.league, title="Title", body="lorem ipsum")

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/news/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/news/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-news-select'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-news-select'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league_admin/article_select.html')

    def test_context(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-news-select'))
        self.assertEqual(response.status_code, 200)
        # Len of empty context --> 2: Fix tests, len context really makes no sense.
        self.assertEqual(len(response.context), 11)
        self.assertTrue(response.context["filter"] is not None)
        self.assertTrue(response.context["paginator"] is not None)
        self.assertTrue(response.context["all_articles"] is not None)
        # self.assertEqual(response.context["filter"], ArticleFilter)


    def test_pagination_is_ten(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-news-select'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("paginator" in response.context)
        # self.assertTrue(response.context["paginator"] == True)
        self.assertEqual(len(response.context['paginator'].page(1)), 10)

    def test_pagination_page_2(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('league-admin-news-select')+"?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("paginator" in response.context)
        # self.assertTrue(response.context["is_paginated"] == True)
        #0 Original rosters plus 13 create --> 13, 10 and 3
        self.assertEqual(len(response.context['paginator'].page(2)), 3)



