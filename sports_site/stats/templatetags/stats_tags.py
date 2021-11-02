from django import template
from league.models import SeasonStage

register = template.Library()

@register.filter(name='get_stage')
def get_stage(value):
    return SeasonStage.objects.get(pk=value)