from django import template
from league.models import SeasonStage

register = template.Library()

@register.filter(name='get_stage')
def get_stage(value):
    """
    Template tag used on the stats page, to get the the stage of a 
    filtered season that otherwise wouldn't have been initially passed
    onto the view and rendered.
    Used in: pitching_stats_page.html, stats_page.html
    team_pitching_stats_page.html, team_stast_page.html, standing_page.html.
    """
    return SeasonStage.objects.get(pk=value)