import django_filters
from league.models import Season, SeasonStage
from .models import PlayerHittingGameStats, PlayerPitchingGameStats, TeamGameStats


def LeagueSeason(request):
    if request is None:
        return Season.objects.none()

    league = request.GET.get("league", None)
    return Season.objects.filter(league__url=league)


def _league_stage(request):
    """
    Filters SeasonStage objects by the league.
    Used in HittingAdvancedFilter, Hitting/PitchingSimpleFilter
    """
    if request is None:
        return SeasonStage.objects.none()

    league = request.GET.get("league", None)
    return SeasonStage.objects.filter(season__league__url=league)


class HittingAdvancedFilter(django_filters.FilterSet):
    season = django_filters.ModelChoiceFilter(
        field_name="season__season",
        label="Season",
        queryset = LeagueSeason
            )

    stage = django_filters.ModelChoiceFilter(
        field_name="season__stage",
        label="Stage",
        queryset = _league_stage
            )

    def __init__(self, *args, **kwargs):
        self.league = kwargs.pop('league')
        # season.queryset = Season.objects.all().filter(league__url=self.league)
        super(HittingAdvancedFilter, self).__init__(*args, **kwargs)
        print(args, kwargs)


    class Meta:
        model = PlayerHittingGameStats
        fields = ["season", "stage"]


class HittingSimpleFilter(django_filters.FilterSet):
    """
    Used stats/views/views.py
        StatsView()
    """
    season = django_filters.ModelChoiceFilter(
        field_name="season",
        label=False,
        empty_label="Stage",
        queryset = _league_stage
            )

    class Meta:
        model = PlayerHittingGameStats
        fields = ["season",]


class PitchingSimpleFilter(django_filters.FilterSet):
    """
    Used stats/views/views.py
        PitchingStatsView()
    """
    season = django_filters.ModelChoiceFilter(
        field_name="season",
        label=False,
        empty_label="Stage",
        queryset = _league_stage
            )

    class Meta:
        model = PlayerPitchingGameStats
        fields = ["season",]


class StandingsSimpleFilter(django_filters.FilterSet):
    """
    Used stats/views/views.py
        StatsView()
    """
    season = django_filters.ModelChoiceFilter(
        field_name="season",
        label=False,
        empty_label="Stage",
        queryset = _league_stage
            )

    class Meta:
        model = TeamGameStats
        fields = ["season",]



