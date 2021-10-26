import django_filters
from django import forms
from .models import PlayerHittingGameStats, PlayerPitchingGameStats
from league.models import Season, SeasonStage, League



# def league(request):
#     league_slug = request.GET.get('league', None)
#     league = League.objects.all().filter(url=league_slug)
#     print(league)
#     return league
# season__season__league = django_filters.ModelChoiceFilter(queryset=league)
    # league = django_filters.ModelChoiceFilter(field_name='season__season__league',
        # queryset=League.objects.all())

class HittingSeasonFilter(django_filters.FilterSet):
    class Meta:
        model = PlayerHittingGameStats
        fields = ["season__season", "season__stage"]


class SeasonFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        print(f"+++++++++++++++++++++{kwargs}")
        season_queryset = kwargs.pop("season", None)
        super(SeasonFilterForm, self).__init__(*args, **kwargs)
        self.fields['Season'] = forms.ModelChoiceField(
            queryset=season_queryset,
            label=False,
            required=False,
            )

    def process(self):
        pass


