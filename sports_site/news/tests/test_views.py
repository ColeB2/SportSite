from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse
from league.models import Game, League, SeasonStage
from news.models import Article



class HomeViewTest(TestCase):
    """
    Tests home from news/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.article = Article.objects.create(league=cls.league, title="Article Title", body="lorem ipsum", author="Me")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('news-home')+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('news-home')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/home.html')

    def test_context(self):
        league_articles = Article.objects.filter(league=self.league).order_by('-id')[:10]
        fs = SeasonStage.objects.get(season__league=self.league, featured=True)
        sc_query = Game.objects.filter(season=fs).query
        sc_query.group_by = ["date"]
        schedule = QuerySet(query=sc_query, model=Game)

        response = self.client.get(reverse('news-home')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.league, response.context["league"])
        self.assertEqual(league_articles, response.context["articles"])
        self.assertQuerysetEqual(schedule, response.context["schedule"])
        #TodoStats:
        print(response.context["stats"])


class NewsDetailTest(TestCase):
    """
    Tests news_detail from news/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.article = Article.objects.create(league=cls.league, title="Article Title", body="lorem ipsum", author="Me")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/news/article-title?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('news-detail', kwargs={"slug":"article-title"})+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('news-detail', kwargs={"slug":str(self.article.slug)})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')

    def test_context(self):
        response = self.client.get(reverse('news-detail', kwargs={"slug":str(self.article.slug)})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["league"], self.league)
        self.assertEqual(response.context["article"], self.article)


class ArticleCreateViewTest(TestCase):
    """
    Tests ArticleCreateView from news/views.py
    """
    @classmethod
    def setUpTestData(cls):
        pass


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        print(f"login {login}")
        response = self.client.get('/league/news/create/article')
        self.assertEqual(response.status_code, 200)

    def test_viewing_without_perm(self):
        response = self.client.get('/league/news/create/article')
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_detail/home.html')

