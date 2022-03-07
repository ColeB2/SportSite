from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, TemplateView
from league.models import League
from ..forms import LeagueHittingOptionsForm, LeagueHittingStatsOptionsForm
from ..models import LeagueHittingOptions, LeagueHittingStatsOptions


def league_admin_options_view(request):
    """Currently Deprecated infavour of CBV"""
    league = League.objects.get(admin=request.User)
    options = LeagueHittingOptions.objects.get(league = league)

    context = {
        "league": league,
        "options": options,
        }
    return render(request, "league_admin/options.html", context)



"""Options Views --> move own folder in future"""
class OptionsView(TemplateView):
    template_name = "league_admin/options.html"

    def dispatch(self, request, *args, **kwargs):
        self.league = League.objects.get(admin=self.request.user)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options'] = LeagueHittingOptions.objects.get(league=self.league)
        return context


class HittingOptionsFormView(FormView):
    template_name = "league_admin/options.html"
    form_class = LeagueHittingOptionsForm
    success_url = reverse_lazy("league-admin-options")

    def form_valid(self, form):
        form.process()
        return super().form_valid(form)

class HittingOptionsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'league.league_admin'
    template_name = "league_admin/option_templates/options_update.html"
    form_class = LeagueHittingOptionsForm
    model = LeagueHittingOptions
    success_url = reverse_lazy("league-admin-options")

"""hitting stat options"""
class HittingStatsOptionsUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Used for custom stats, gives options to turn on specific stats
    for a more customizable website.
    """
    permission_required = 'league.league_admin'
    template_name = "league_admin/option_templates/options_update.html"
    form_class = LeagueHittingStatsOptionsForm
    model = LeagueHittingStatsOptions
    success_url = reverse_lazy("league-admin-hitting-options")