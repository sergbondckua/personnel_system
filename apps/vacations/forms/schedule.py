from django import forms

from apps.common.forms import (
    MonthField,
    YearField,
)


class VacationScheduleFilterForm(forms.Form):
    """
    Фільтр графіка відпусток.
    """

    year = YearField()

    month = MonthField()