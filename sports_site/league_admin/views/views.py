from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render#, redirect
from ..filters import RosterFilter
from league.models import (League, Roster)



@login_required
@permission_required('league.league_admin')
def league_admin_dashboard_view(request):
    context = {}
    return render(request, "league_admin/dashboard.html",context)

@login_required
@permission_required('league.league_admin')
def league_admin_roster_select(request):
    league = League.objects.get(admin=request.user)
    f = RosterFilter(request.GET, queryset=Roster.objects.all().filter(team__team__league=league) )
    roster_list = f.qs

    paginator = Paginator(roster_list, 10)
    page = request.GET.get('page', 1)

    try:
        all_rosters = paginator.page(page)
    except PageNotAnInteger:
        all_rosters = paginator.page(1)
    except EmptyPage:
        all_rosters = paginator.page(paginator.num_pages)


    context = {
        "filter": f,
        "paginator": paginator,
        "all_rosters": all_rosters
        }
    return render(request, "league_admin/roster_select.html", context)



