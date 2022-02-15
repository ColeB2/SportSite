from django.test import TestCase
from django.urls import reverse
from league.models import League
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
        league_articles = Article.objects.filter(league__url=self.league.slug).order_by('-id')[:10]

        response = self.client.get(reverse('news-home')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.league, response.context["league"])
        self.assertEqual(league_articles, response.context["articles"])
        #TodoStats: