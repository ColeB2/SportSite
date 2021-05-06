from django import forms

from league.models import Season, SeasonStage, Game

class SeasonSelectForm(forms.ModelForm):
    class Meta:
        model = SeasonStage
        fields = ['season', 'stage',]

    def __init__(self, *args, **kwargs):
        super(SeasonSelectForm(*args, **kwargs))
        self.fields['season'].required = False
        self.fields['stage'].required = False



class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['home_team', 'away_team', 'date', 'start_time',
        'location', 'stats_entered', 'final_score']


class SeasonCreateForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['year',]


class SeasonStageCreateForm(forms.ModelForm):
    class Meta:
        model = SeasonStage
        fields = ['stage']
