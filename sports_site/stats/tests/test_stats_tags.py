from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django.urls import reverse

from league.models import League, SeasonStage, Season
from stats.templatetags.stats_tags import get_stage



class TestStatsTags(TestCase):
    def test_get_stage(self):
        def render_template(string,context=None):
            context = context or {}
            context = Context(context)
            return Template(string).render(context)

        league = League.objects.get(id=1)
        stage = SeasonStage.objects.get(id=2)
        factory = RequestFactory()
        req = factory.get(f'/league/stats/?season={stage.pk}&league={league.url}')

        rendered = render_template(
            '{% load stats_tags %}'
            '{% if request.GET.season %} {{request.GET.season|get_stage}}'
            '{% endif %}',
            {"league": league, "stage": stage, "request": req}

        )
        self.assertIn(str(stage), rendered)

