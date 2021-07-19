from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import router
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from ..filters import PlayerFilter
from ..forms import (TeamCreateForm)
from league.models import (League, Player)
from user.models import UserProfile
from ..decorators import user_owns_player



@permission_required('league.league_admin')
def league_admin_team_create_view(request):
    league = request.user.userprofile.league
    league_users = User.objects.all().filter(userprofile__league=league)

    if request.method == 'POST':
        form = TeamCreateForm(data=request.POST)
        form.fields['owner'].queryset=league_users
        if form.is_valid():
            new_team = form.process(league=league)
            messages.success(request, f"{new_team} created.")

        # next=request.POST.get('next', '/')
        # return HttpResponseRedirect(next)
        return redirect('league-admin-dashboard')

    else:
        form = TeamCreateForm()
        form.fields['owner'].queryset=league_users
    context = {
        "form": form,
        "lu":league_users
    }
    return render(request, "league_admin/team_create.html", context)