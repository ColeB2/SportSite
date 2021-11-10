from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserRegistrationForm

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user_auth/password_reset.html'
    email_template_name = 'user_auth/password_reset_email.html'
    subject_template_name = 'user_auth/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')






# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('news-home')
    else:
        form = UserRegistrationForm()
    context = {
        "form" : form
    }
    return render(request, "user_auth/register.html", context)

