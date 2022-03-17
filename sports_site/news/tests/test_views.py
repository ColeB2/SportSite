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
        cls.article = Article.objects.create(
            league=cls.league,
            title="Article Title",
            body="lorem ipsum",
            author="Me")

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
        league_articles = Article.objects.filter(
            league=self.league).order_by('-id')[:10]
        fs = SeasonStage.objects.get(season__league=self.league, featured=True)
        sc_query = Game.objects.filter(season=fs).query
        sc_query.group_by = ["date"]
        schedule = QuerySet(query=sc_query, model=Game)

        response = self.client.get(reverse('news-home')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.league, response.context["league"])
        self.assertQuerysetEqual(league_articles, response.context["articles"])
        self.assertQuerysetEqual(
            schedule, response.context["schedule"], ordered=False)
        #TodoStats:
        print(response.context["stats"])


class NewsDetailTest(TestCase):
    """
    Tests news_detail from news/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.article = Article.objects.create(
            league=cls.league,
            title="Article Title",
            body="lorem ipsum",
            author="Me")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/news/article-title?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse(
            'news-detail', kwargs={"slug":"article-title"})+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(
            'news-detail', kwargs={"slug":str(self.article.slug)})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')

    def test_context(self):
        response = self.client.get(reverse(
            'news-detail', kwargs={"slug":str(self.article.slug)})+"?league=TL")
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
        response = self.client.get('/league/news/create/article')
        self.assertEqual(response.status_code, 200)

    def test_viewing_without_perm(self):
        response = self.client.get('/league/news/create/article')
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/new_article.html')

    def test_success_url(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)

        post = {"title": "TitleOne",
                "body": "Lorem ipsum"}


        response = self.client.post(
            '/league/news/create/article', post, follow=True)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.get(reverse(
            'news-detail', kwargs={"slug":"titleone"})+"?league=TL")
        self.assertEqual(response2.status_code, 200)

        # response = self.client.get(reverse('news-home')+"?league=TL")
        # self.assertEqual(response.status_code, 200)
        #self.assertRedirects(response, "/league/?league=TL")




class ArticleEditViewTest(TestCase):
    """
    Tests ArticleEditView from news/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.article = Article.objects.create(
            league=cls.league,
            title="Article Title",
            body="lorem ipsum",
            author="Me")


    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/news/article-title/edit?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_viewing_without_perm(self):
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/article_edit.html')


    def test_success_url(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)

        post = {"title": "TitleOne",
                "body": "Lorem ipsum",
                "author": "You"}

        response = self.client.post(reverse(
            'news-edit',
            kwargs={"slug": self.article.slug})+"?league=TL",
            post,
            follow=True)

        self.assertEqual(response.status_code, 200)
        edited_article = Article.objects.all()[0]
        self.assertEqual(edited_article.title, "TitleOne")

        #self.assertRedirects(response, "/league/?league=TL")


class ArticlesView(TestCase):
    """
    Tests ArticlesView from news/views.py
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        for i in range(13):
            article = Article.objects.create(
                league=cls.league,
                title="Article Title",
                body="lorem ipsum",
                author="Me")


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/league/news/?league=TL')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('news-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('news-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_page.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('news-page')+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context['articles']), 10)

    def test_pagination_page_2(self):
        response = self.client.get(reverse('news-page')+"?league=TL&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context['articles']), 3)


class ArticleDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.article = Article.objects.create(
            league=cls.league,
            title="Article Title",
            body="lorem ipsum",
            author="Me")



    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get('/league/news/article-title/delete?league=TL')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-delete', kwargs={"slug":"article-title"})+"?league=TL")
        self.assertEqual(response.status_code, 200)


    def test_viewing_without_perm(self):
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 302)


    def test_view_uses_correct_template(self):
        login = self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-delete', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/confirm_delete.html')


    def test_article_delete(self):
        login = self.client.login(username="Test", password="test")

        response = self.client.get(reverse(
            'news-delete', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse(
            'news-delete', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 302)


        # response = self.client.get(reverse('news-delete', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(len(Article.objects.all()), 0)
        self.assertEqual(response.context, None)
