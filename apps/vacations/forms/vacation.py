from django import forms

from apps.vacations.models import Vacation


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation

        fields = (
            "person",
            "vacation_type",
            "date_from",
            "date_to",
            "notes",
        )

        widgets = {
            "date_from": forms.DateInput(attrs={"type": "date"}),
            "date_to": forms.DateInput(attrs={"type": "date"}),
            "order_date": forms.DateInput(attrs={"type": "date"}),
        }


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields["person"].widget.attrs["class"] = "form-select"
    self.fields["vacation_type"].widget.attrs["class"] = "form-select"

    self.fields["date_from"].widget.attrs["class"] = "form-control"
    self.fields["date_to"].widget.attrs["class"] = "form-control"

    self.fields["notes"].widget.attrs["rows"] = 3
