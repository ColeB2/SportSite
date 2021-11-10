from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from user.models import UserProfile
from league.models import League
 
 
 
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    league = forms.CharField(label="League Name")
    league_url = forms.SlugField(label="League URL",
        help_text="Shortened League url used  to find your league. Ex. sport.pythonanywhere.com/<MLB>, must be unique from other leagues.")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'league', 'league_url']
        
        
    
    def save(self, commit=True):
        #change from false when ready to go
        user = super(UserRegistrationForm, self).save(commit=commit)
        league = self.cleaned_data['league']
        league_url = self.cleaned_data['league_url']
        
        user_league = League(league=league, admin=user, url=league_url)
        user_league.save()
        user_profile = UserProfile(user=user, league=user_league)
        user_profile.save()
        
        return user, user_profile, user_league
        
