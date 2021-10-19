import django_filters
from django import forms
from .models import PlayerHittingGameStats, PlayerPitchingGameStats
from league.models import Season, SeasonStage

class HittingSeasonFilter(django_filters.FilterSet):
    class Meta:
        model = PlayerHittingGameStats
        fields = ["season"]


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


