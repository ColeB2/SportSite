import django_filters
from league.models import Player, Roster, SeasonStage
from news.models import Article



class ArticleFilter(django_filters.FilterSet):
    #todo - implement date
    #date_posted = django_filters.DateFromToRangeFilter
    class Meta:
        model = Article
        fields = ["title",]# "date_posted"]


class PlayerFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Player
        fields = ["last_name", "first_name"]


def league_seasons(request):
    if request is None:
        return SeasonStage.objects.none()
    league = request.user.userprofile.league
    return SeasonStage.objects.filter(season__league=league)


class RosterFilter(django_filters.FilterSet):
    team__season = django_filters.ModelChoiceFilter(queryset=league_seasons)
    class Meta:
        model = Roster
        fields = ["team__season",]


    def __init__(self, *args, **kwargs):
        super(RosterFilter, self).__init__(*args, **kwargs)
        self.filters['team__season'].label="Season"





