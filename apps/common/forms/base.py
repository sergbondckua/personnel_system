from __future__ import annotations

from django import forms


class BaseChoiceField(forms.TypedChoiceField):
    """
    Базове поле вибору.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        )

        super().__init__(*args, **kwargs)
