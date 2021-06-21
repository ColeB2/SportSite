from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Row, Column)
from django import forms
from .models import PlayerHittingGameStats
from league.models import PlayerSeason


class PlayerStatsCreateForm(forms.Form):
    """Creates all player stats objects to be edited later"""
    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('team_game_stats')
        super(PlayerStatsCreateForm, self).__init__(*args, **kwargs)
        self.player_queryset = PlayerSeason.objects.all().filter(team__team=self._team_season)

        self.fields["player"] = forms.ModelChoiceField(
            queryset=self.player_queryset,
            label=False,
            required=False,
            )

        self.fields["pitched"] = forms.BooleanField(
            required=False,
            )

        #crispy layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-5"),
                Column("pitched", css_class="form-group col-md-4"),
                css_class="form-row"
                ),
            )
        self.helper.form_tag = False



    def process(self):
        pass




class PlayerHittingGameStatsForm(forms.ModelForm):
    class Meta:
        model = PlayerHittingGameStats
        exclude = ['team_stats', 'season', 'average','on_base_percentage',
            'slugging_percentage', 'on_base_plus_slugging', 'hits',
        ]

    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('team_game_stats')
        super(PlayerHittingGameStatsForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = PlayerSeason.objects.all().filter(team__team=self._team_season)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-6"),
                css_class="form-row"
                ),
            Row(
                Column("plate_appearances"),
                Column("at_bats"),
                Column("singles"),
                Column("doubles"),
                Column("triples"),
                Column("homeruns"),
                Column("strikeouts"),
                Column("walks"),
                Column("hit_by_pitch"),
                css_class="form-row"),
            Row(
                Column("runs_batted_in"),
                Column("runs"),
                Column("stolen_bases"),
                Column("caught_stealing"),
                Column("sacrifice_flies"),
                Column("sacrifice_bunts"),
                Column("reached_on_error"),
                Column("fielders_choice"),
                css_class="form-row"),
            )
        self.helper.form_tag = False


    def process(self):
        if self.cleaned_data.get("player"):
            # Player selector is not none: create player, team game to current game.
            playerhittinggamestats = self.save(commit=False)
            if playerhittinggamestats.team_stats is None:
                playerhittinggamestats.team_stats = self._team_game_stats
            playerhittinggamestats.save()
            return playerhittinggamestats
