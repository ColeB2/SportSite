from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from user.models import UserProfile
 
 
 
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    league = forms.CharField(label="League Name")
    league_url = forms.SlugField(label="League URL", 
        help_text="Shortened League url used  to find your league. Ex. sport.pythonanywhere.com/<MLB>, must be unique from other leagues.")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'league', 'league_url']
        
