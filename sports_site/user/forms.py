from django import forms
from league.models import Roster, TeamSeason, PlayerSeason, Player

from django.forms.models import inlineformset_factory, formset_factory #test
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

class RosterTestForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['team',]

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False #crucial?
        helper.layout = Layout(Fieldset('Create New Roster', 'team'),)

        return helper

class PlayerFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PlayerFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Fieldset('Add Player','player','season'),
            )

PlayerTestFormset = inlineformset_factory(Roster, PlayerSeason, fields=('player','season',),extra=2, can_delete=False,)


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


class CreatePlayerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreatePlayerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=35)
        self.fields['last_name'] = forms.CharField(max_length=35)











