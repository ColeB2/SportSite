from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from user.models import UserProfile
from league.models import League



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self, commit=True):
        #change from false when ready to go

        user = super(UserRegistrationForm, self).save(commit=commit)
        user_league = League(name=league, admin=user, url=league_url)
        user_league.save()
        user_profile = UserProfile(user=user, league=user_league)
        user_profile.save()

        return user, user_profile, user_league

