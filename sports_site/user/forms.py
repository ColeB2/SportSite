from django import forms
from league.models import Roster, TeamSeason, PlayerSeason, Player


class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['team',]

    def __init__(self, user, *args, **kwargs):
        super(RosterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['team'].queryset = TeamSeason.objects.filter(team__owner=user)


class PlayerSelectForm(forms.Form):
    def __init__(self, exclude_list=[], *args, **kwargs):
        super(PlayerSelectForm,self).__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelChoiceField(
            queryset=Player.objects.all().exclude(id__in=[o.id for o in exclude_list]),
            label=False,
            required=False,
            )

        self.fields['players'].widget.attrs.update(style='max-width: 24em')


class PlayerCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlayerCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=35)
        self.fields['last_name'] = forms.CharField(max_length=35)


class PlayerDeleteForm(forms.Form):
    def __init__(self, roster_queryset, *args, **kwargs):
        super(PlayerDeleteForm,self).__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelChoiceField(
            # queryset=Player.objects.all(),
            queryset=roster_queryset,
            label=False,
            required=False,
            )

        self.fields['players'].widget.attrs.update(style='max-width: 24em')


class PlayerSeasonForm(forms.ModelForm):

    class Meta:
        model = PlayerSeason
        fields = ['player', 'team']


class RosterSelectForm(forms.Form):
    def __init__(self,roster_queryset, *args, **kwargs):
        super(RosterSelectForm, self).__init__(*args, **kwargs)
        self.fields['roster'] = forms.ModelChoiceField(
            queryset=roster_queryset,
            label="Select Roster:",
            required=False,
            )

class RosterCreateForm(forms.Form):
    def __init__(self, season_queryset, roster_queryset, *args, **kwargs):
        super(RosterCreateForm, self).__init__(*args, **kwargs)
        self.fields['seasons'] = forms.ModelChoiceField(
            queryset=season_queryset,
            label="Select a season to create your roster for:",
            required=True,
            )
        self.fields['roster'] = forms.ModelChoiceField(
            queryset=roster_queryset,
            label="Select a roster you want to copy over(optional):",
            required=False,
            )













