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
        #Todo Stats:
        # print(response.context["stats"])
        print(f"ToDo: news, test_views stats context")


    def test_league_no_stats(self):
        """Tests what happens for a leagues homepage with nothing created"""
        League.objects.create(name="T", url="TT")
        response = self.client.get(reverse('news-home')+"?league=TT")
        self.assertEqual(response.status_code, 200)


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
        cls.league = League.objects.get(id=1)


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/news/create/article')
        self.assertEqual(response.status_code, 200)

    def test_viewing_without_perm(self):
        response = self.client.get('/league/news/create/article')
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse('news-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/new_article.html')

    def test_article_create(self):
        self.client.login(username="Test", password="test")
        article_len = Article.objects.filter(league=self.league).count()

        post = {
            "league": self.league,
            "title": "TitleOne",
            "body": "Lorem ipsum",
            "author": "Me"
            }

        response = self.client.post(reverse("news-create"), 
            post,
            follow=True)

        article = Article.objects.get(league=self.league, title=post["title"])
        self.assertEqual(article.league, self.league)
        self.assertEqual(article.title, post["title"])
        self.assertEqual(article.body, post["body"])
        self.assertEqual(article.author, post["author"])

        article_len_create = Article.objects.filter(league=self.league).count()
        self.assertEqual(article_len + 1, article_len_create)
        self.assertRedirects(response, reverse('news-home')+"?league=TL")


    def test_success_url(self):
        self.client.login(username="Test", password="test")

        post = {"title": "TitleOne",
                "body": "Lorem ipsum",
                "author": "You"}

        response = self.client.post(reverse('news-create')+"?league=TL",
            post,
            follow=True)

        self.assertRedirects(response, reverse('news-home')+"?league=TL")

    def test_success_url2(self):
        """Tests get_success_url without provided league queryset"""
        self.client.login(username="Test", password="test")

        post = {"title": "TitleOne",
                "body": "Lorem ipsum",
                "author": "You"}

        response = self.client.post(reverse('news-create'),
            post,
            follow=True)
        
        self.assertRedirects(response, reverse('news-home')+"?league=TL")




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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/news/article-title/edit?league=TL')
        self.assertEqual(response.status_code, 200)

    def test_viewing_anonymous_user(self):
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 403)

    def test_user_viewing_without_perm(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 403)

    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/article_edit.html')


    def test_article_edit(self):
        self.client.login(username="Test", password="test")
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


    def test_success_url(self):
        self.client.login(username="Test", password="test")

        post = {"title": "TitleOne",
                "body": "Lorem ipsum",
                "author": "You"}

        response = self.client.post(reverse(
            'news-edit',
            kwargs={"slug": self.article.slug})+"?league=TL",
            post,
            follow=True)

        self.assertRedirects(response, reverse('news-home')+"?league=TL")

    def test_success_url2(self):
        """Tests get_success_url without provided league queryset"""
        self.client.login(username="Test", password="test")

        post = {"title": "TitleOne",
                "body": "Lorem ipsum",
                "author": "You"}

        response = self.client.post(reverse(
            'news-edit',
            kwargs={"slug": self.article.slug}),
            post,
            follow=True)
        
        self.assertRedirects(response, reverse('news-home')+"?league=TL")


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
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/news/article-title/delete?league=TL')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-delete', kwargs={"slug":"article-title"})+"?league=TL")
        self.assertEqual(response.status_code, 200)


    def test_viewing_anonymous_user(self):
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 403)

    
    def test_user_viewing_without_perm(self):
        self.client.login(username="BadUser", password="bad")
        response = self.client.get(reverse(
            'news-edit', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 403)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'news-delete', kwargs={"slug": self.article.slug})+"?league=TL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/confirm_delete.html')


    def test_article_delete(self):
        article_count = Article.objects.filter(league=self.league).count()

        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
            'news-delete', 
            kwargs={"slug": self.article.slug})+"?league=TL", follow=True)
        self.assertRedirects(response, reverse('news-home')+"?league=TL")

        article_count_del = Article.objects.filter(league=self.league).count()
        self.assertEqual(article_count-1, article_count_del)

    def test_success_url(self):
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
            'news-delete', 
            kwargs={"slug": self.article.slug})+"?league=TL", follow=True)
        
        self.assertRedirects(response, reverse('news-home')+"?league=TL")

    def test_success_url2(self):
        """Test redirect without provided league queryset"""
        self.client.login(username="Test", password="test")
        response = self.client.post(reverse(
            'news-delete', 
            kwargs={"slug": self.article.slug}), follow=True)
        
        self.assertRedirects(response, reverse('news-home')+"?league=TL")
