from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Row, Column, MultiWidgetField, HTML)
from django import forms
from .models import PlayerHittingGameStats
from league.models import PlayerSeason



class PlayerHittingGameStatsForm(forms.ModelForm):
    class Meta:
        model = PlayerHittingGameStats
        exclude = ['team_stats', 'season', 'average','on_base_percentage',
            'slugging_percentage', 'on_base_plus_slugging', 'at_bats',
            'plate_appearances', 'hits',
        ]

    def __init__(self, *args, **kwargs):
        team_season_pk = kwargs.pop('team_season_pk')
        super(PlayerHittingGameStatsForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = PlayerSeason.objects.all().filter(team__team=team_season_pk)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-2"),


                Column("singles"),
                Column("doubles"),
                Column("triples"),
                Column("homeruns"),
                Column("strikeouts"),
                Column("walks"),
                Column("hit_by_pitch"),
                css_class="form-row"
                ),
            Row(

                Column("runs_batted_in"),
                Column("runs"),
                Column("stolen_bases"),
                Column("caught_stealing"),


                Column("sacrifice_flies"),
                Column("sacrifice_bunts"),
                Column("reached_on_error"),
                Column("fielders_choice"),

                css_class="form-row"
                )


            )