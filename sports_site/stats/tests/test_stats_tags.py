from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse

from league.models import League, SeasonStage, Season
from stats.templatetags.stats_tags import get_stage



class TestStatsTags(TestCase):
    def test_get_stage(self):
        def render_template(string,context=None):
            context = context or {}
            context = Context(context)
            return Template(string).render(context)

        rendered = render_template(
            '{% load stats_tags %}'
            '{% if request.GET.season %} {{request.GET.season|get_stage}}'
            '{% endif %}'
        )
        print(rendered)
        league = League.objects.get(id=1)
        stage = SeasonStage.objects.get(id=3)
        t = Template(
            '{% load stats_tags %}'
            '{% if request.GET.season %} {{request.GET.season|get_stage}}'
            '{% endif %}'
        )
        c = Context({})
        t.render(c)
        # print(c['season'])
        # print('XXX')
        # print(t)
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'stats-page')+f'?league={league.url}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stats/stats_page.html")
        # print(response)


    def test_other_season(self):
        """from test_views, tinkering."""
        league = League.objects.get(id=1)
        stage = SeasonStage.objects.get(id=2)
        self.client.login(username="Test", password="test")
        response = self.client.get(reverse(
            'stats-page') + f'?season={stage.pk}&league={league.url}')
        self.assertEqual(response.status_code, 200)


        #Tests get_state tag, which should change the title of the table
        title = (
            f'<h3 class="text-center">' +
            f'{stage}'+
            f'</h3>'
            )

        self.assertInHTML(title, response.content.decode())
        self.assertInHTML("2022 Postseason", response.content.decode())

