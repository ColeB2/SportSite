from datetime import datetime, time
from django.test import TestCase
from django.contrib.auth.models import User
from league.models import (Game, League, Player, PlayerSeason, Roster, Season,
    SeasonStage, Team, TeamSeason)
from stats.models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameStats, TeamGameLineScore)
from news.models import Article



class ArticleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.article = Article.objects.create(league=cls.league, title="Article Title", body="lorem ipsum", author="Me")

    def test_created_properly(self):
        self.assertEqual(self.article.title, "Article Title")
        self.assertEqual(self.article.body, "lorem ipsum")
        self.assertEqual(self.article.author, "Me")

    def test_fk_points_proper_place(self):
        self.assertEqual(self.article.league, self.league)

    def test_labels(self):
        league_label = self.article._meta.get_field('league').verbose_name
        title_label = self.article._meta.get_field('title').verbose_name
        body_label = self.article._meta.get_field('body').verbose_name
        image_label = self.article._meta.get_field('image').verbose_name
        image_description_label = self.article._meta.get_field('image_description').verbose_name
        date_posted_label = self.article._meta.get_field('date_posted').verbose_name
        author_label = self.article._meta.get_field('author').verbose_name
        slug_label = self.article._meta.get_field('slug').verbose_name
        self.assertEqual(league_label, "league")
        self.assertEqual(title_label, "title")
        self.assertEqual(body_label, "body")
        self.assertEqual(image_label, "image")
        self.assertEqual(image_description_label, "image description")
        self.assertEqual(date_posted_label, "date posted")
        self.assertEqual(author_label, "author")
        self.assertEqual(slug_label, "slug")

    def test_defaults(self):
        default = self.article._meta.get_field("image").default
        self.assertEqual(default, "article_images/baseballplaceholder2.png")

    def test_max_length(self):
        title_max_length = self.article._meta.get_field("title").max_length
        image_description_max_length = self.article._meta.get_field("image_description").max_length
        author_max_length = self.article._meta.get_field("author").max_length
        self.assertEqual(title_max_length, 200)
        self.assertEqual(image_description_max_length, 200)
        self.assertEqual(author_max_length, 50)

    def test_expected_name(self):
        self.assertEqual(str(self.article), "Article Title")

    def test_get_absolute_url(self):
        self.assertEqual(self.article.get_absolute_url(), '/league/news/article-title')