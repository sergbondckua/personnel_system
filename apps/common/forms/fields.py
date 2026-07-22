from __future__ import annotations

from datetime import date

from django import forms

from .base import BaseChoiceField
from .choices import month_choices
from .choices import year_choices


class YearField(BaseChoiceField):
    """
    Поле вибору року.
    """

    def __init__(self, *args, **kwargs):
        today = date.today()

        kwargs.setdefault("label", "Рік")
        kwargs.setdefault("choices", year_choices())
        kwargs.setdefault("coerce", int)
        kwargs.setdefault("initial", today.year)

        super().__init__(*args, **kwargs)


class MonthField(BaseChoiceField):
    """
    Поле вибору місяця.
    """

    def __init__(self, *args, **kwargs):
        today = date.today()

        kwargs.setdefault("label", "Місяць")
        kwargs.setdefault("choices", month_choices())
        kwargs.setdefault("coerce", int)
        kwargs.setdefault("initial", today.month)

        super().__init__(*args, **kwargs)