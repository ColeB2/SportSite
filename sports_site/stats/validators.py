from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_innings_pitched(value):
    decimal = round(value % 1)
    if decimal not in [0.1, 0.2]:
        raise ValidationError(
            _('%(decimal)s is not properly fomratted. Innings Pitched value should .1 or .2'),
            params={'decimal': decimal},
            )