import django_filters
from .models import PlayerHittingGameStats, PlayerPitchingGameStats


class HittingSeasonFilter(django_filters.FilterSet):
    class Meta:
        model = PlayerHittingGameStats
        fields = ["season"]