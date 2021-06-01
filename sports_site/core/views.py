from django.shortcuts import render, redirect

# Create your views here.
def landing(request):
    context = {
        }
    return render(request, "core/landing.html", context)


def find_league(request, league_url):
    context = {
        }
    re_url = f"/league/?league={league_url}"
    print(re_url)
    return redirect(re_url)