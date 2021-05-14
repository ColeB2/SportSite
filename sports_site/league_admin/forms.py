from django import forms
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField

from league.models import Season, SeasonStage, Game, Player

class SeasonSelectForm(forms.ModelForm):
    class Meta:
        model = SeasonStage
        fields = ['season', 'stage',]

    def __init__(self, *args, **kwargs):
        super(SeasonSelectForm, self).__init__(*args, **kwargs)
        self.fields['season'].required = False
        self.fields['stage'].required = False


class SeasonCreateForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['year',]


class SeasonStageCreateForm(forms.ModelForm):
    class Meta:
        model = SeasonStage
        fields = ['stage']


class TeamSelectForm(forms.Form):
    def __init__(self, team_queryset, *args, **kwargs):
        super(TeamSelectForm,self).__init__(*args, **kwargs)
        self.fields['teams'] = forms.ModelChoiceField(
            queryset=team_queryset,
            label=False,
            required=False,
            )

        self.fields['teams'].widget.attrs.update(style='max-width: 24em')



class PlayerCreateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name',]

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name',]

class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['home_team', 'away_team', 'date' , 'start_time', 'stats_entered', 'final_score']


class CreateGameForm(forms.Form):
    def __init__(self, team_queryset=None, *args, **kwargs):
        super(CreateGameForm, self).__init__(*args, **kwargs)

        self.fields['home_team'] = forms.ModelChoiceField(
            queryset=team_queryset,
            required = False)

        self.fields['away_team'] = forms.ModelChoiceField(
            queryset=team_queryset,
            required = False)

        cur_date = datetime.datetime.today()
        year_range = tuple([i for i in range(cur_date.year - 5, cur_date.year + 5)])
        self.fields['date'] = forms.DateField(initial=cur_date, widget=forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"), years=(year_range)
            ))
        self.fields['date'].required = False

        self.fields['start_time'] = forms.TimeField(label='Start Time (24:00)', required=False)
        self.fields['location'] = forms.CharField(max_length=20, required=False, label='Location (default: Home)')

        #crispylayout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('home_team', css_class="form-group col-md-4"),
                Column('away_team', css_class="form-group col-md-4"),
                Column('location', css_class="form-group col-md-4"),
                css_class='form-row'
                ),
            Row(
                Column(
                    MultiWidgetField('date', attrs=({'style': 'width: 33%; display: inline-block; '})),
                    css_class='form-group col-md-8'
                    ),
                Column('start_time', css_class='form-group col-md-4'),
                css_class='form-row'
                )
                )

    def process(self, current_stage=None):
        """To be called only after form.is_valid() method has been called"""
        home_data = self.cleaned_data.get('home_team')
        away_data = self.cleaned_data.get('away_team')
        date_data = self.cleaned_data.get('date')
        time_data = self.cleaned_data.get('start_time')
        location_data = self.cleaned_data.get('location')

        if home_data is not None and away_data is not None:

            new_game = Game(season=current_stage, home_team=home_data,
                away_team=away_data, date=date_data)

            if time_data:
                new_game.start_time = time_data
            if location_data:
                new_game.location = location_data

            new_game.save()




