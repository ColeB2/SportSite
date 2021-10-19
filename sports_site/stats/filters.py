import django_filters
from django import forms
from .models import PlayerHittingGameStats, PlayerPitchingGameStats
from league.models import Season, SeasonStage

class HittingSeasonFilter(django_filters.FilterSet):
    season = django_filters.ModelChoiceFilter()
    class Meta:
        model = PlayerHittingGameStats
        fields = ["season"]


class SeasonFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TeamSelectForm,self).__init__(*args, **kwargs)
        self.fields['Season'] = forms.ModelChoiceField(
            queryset=team_queryset,
            label=False,
            required=False,
            )

        self.fields['teams'].widget.attrs.update(style='max-width: 24em')


    def process(self):
        pass


