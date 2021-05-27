import django_filters
from league.models import Roster, Player
from news.models import Article

class RosterFilter(django_filters.FilterSet):
    class Meta:
        model = Roster
        fields = ["team__season",]

    def __init__(self, *args, **kwargs):
        super(RosterFilter, self).__init__(*args, **kwargs)
        self.filters['team__season'].label="Season"


class PlayerFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Player
        fields = ["last_name", "first_name"]


class ArticleFilter(django_filters.FilterSet):
    #todo - implement date
    #date_posted = django_filters.DateFromToRangeFilter
    class Meta:
        model = Article
        fields = ["title",]# "date_posted"]