from django.test import TestCase
from django.urls import reverse

from stats.models import TeamGameLineScore, TeamGameStats


class TeamGameLinescoreCreateView(TestCase):
    """
    Tests team_game_linescore_create_view from stats/views/tg_linescore_views.py

    """