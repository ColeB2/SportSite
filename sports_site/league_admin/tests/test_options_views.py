from django.test import TestCase
from django.urls import reverse

from league.models import League, SeasonStage
from league_admin.models import LeagueHittingOptions


###ToDO after implementation
class LAOptionsView(TestCase):
    """
    Tests OptionsView from league_admin/views/options_views.py

    'options/',
    OptionsView.as_view(), 
    name='league-admin-options
    """
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.get(id=1)
        cls.lho = LeagueHittingOptions.objects.create(league=cls.league)
        return super().setUpTestData()

    def test_view_without_logging_in(self):
        response = self.client.get('/league/admin/options/')
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="Test", password="test")
        response = self.client.get('/league/admin/options/')
        self.assertEqual(response.status_code, 200)


    def test_view_accessible_by_name(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-options"))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-options"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            "league_admin/options.html")


    def test_context(self):
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse("league-admin-options"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["options"], self.lho)

class LAOptionsViewTest(TestCase):
    """
    Tests OptionsView from league_admin/views/options_views.py

    'options/hitting/<int:pk>/edit',
    HittingOptionsUpdateView.as_view(),
    name='league-admin-hitting-options-update'),
    """
    pass
    # def test_view_without_logging_in(self):
    #     response = self.client.get('/league/admin/options/hitting/1/edit')
    #     self.assertEqual(response.status_code, 302)