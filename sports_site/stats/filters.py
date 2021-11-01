import django_filters
from django import forms
from .models import PlayerHittingGameStats, PlayerPitchingGameStats
from league.models import Season, SeasonStage, League




def LeagueSeason(request):
    if request is None:
        return Season.objects.none()

    league = request.GET.get("league", None)
    return Season.objects.filter(league__url=league)


def LeagueStage(request):
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
        queryset = LeagueStage
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
    season = django_filters.ModelChoiceFilter(
        field_name="season",
        label="Stage",
        queryset = LeagueStage
            )

    class Meta:
        model = PlayerHittingGameStats
        fields = ["season",]

