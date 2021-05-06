import django_filters
from league.models import Roster

class RosterFilter(django_filters.FilterSet):
    class Meta:
        model = Roster
        fields = ["team__season",]

    def __init__(self, *args, **kwargs):
        super(RosterFilter, self).__init__(*args, **kwargs)
        self.filters['team__season'].label="Season"