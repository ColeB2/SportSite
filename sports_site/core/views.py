from django.shortcuts import redirect, render


def landing(request):
    context = {
        }
    return render(request, "core/landing.html", context)


def find_league(request, league_url):
    re_url = f"/league/?league={league_url}"
    return redirect(re_url)


def login_redirect(request):
    if request.user.has_perm('league.league_admin'):
        return redirect("league-admin-dashboard")
    else:
        return redirect("user-dashboard")