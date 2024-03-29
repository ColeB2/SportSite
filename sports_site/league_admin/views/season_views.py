from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import router
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, UpdateView
from ..forms import SeasonForm
from league.models import League, Season
from ..decorators import user_owns_season



class SeasonView(PermissionRequiredMixin, ListView):
    permission_required = "league.league_admin"
    template_name = "league_admin/season_templates/season_page.html"
    model = Season


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = League.objects.get(admin=self.request.user)
        context['seasons'] = Season.objects.filter(league=league).order_by('-id')
        return context


@permission_required('league.league_admin')
def league_admin_create_season_view(request):
    seasons = Season.objects.filter(league__admin=request.user).order_by('-id')

    if request.method == 'POST':
        form = SeasonForm(data = request.POST)
        if form.is_valid():
            new_season, created = form.process(
                league=request.user.userprofile.league)

            if created:
                messages.success(request, f"{new_season} created.")
            else:
                messages.info(request, f"{new_season} already exists.")

        return redirect('league-admin-season')
    else:
        form = SeasonForm()

    context = {
        'seasons':seasons,
        'form': form
    }
    return render(request, "league_admin/season_templates/season_create.html",
                  context)


@permission_required('league.league_admin')
@user_owns_season
def league_admin_season_delete_info_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)

    using = router.db_for_write(season._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([season])

    if request.method == 'POST':
        season.delete()
        messages.success(request,
                         f"{season} and all related objects were deleted.")
        return redirect('league-admin-season')

    context = {
        'season':season,
        'nested_object':nested_object,
    }
    return render(request, "league_admin/season_templates/season_delete.html",
                  context)


class SeasonEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'league.league_admin'
    template_name = 'league_admin/season_templates/season_edit.html'
    model = Season
    form_class = SeasonForm


    @method_decorator(user_owns_season)
    def dispatch(self, *args, **kwargs):
        return super(SeasonEditView, self).dispatch(*args, **kwargs)


    def get_success_url(self):
        url = reverse('league-admin-season-stage',
                      args=[self.object.year, self.object.pk])
        return url

