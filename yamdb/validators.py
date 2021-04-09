from datetime import datetime
from django.core.exceptions import ValidationError


def validate_date(value):
    now = datetime.now()
    year = int(now.strftime("%Y"))
    if value > year:
        raise ValidationError(
            f' Вы не можете ввести давту из будующего. Ваша дата: {value}'
        )
    return value
