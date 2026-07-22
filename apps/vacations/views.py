from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.vacations.schedule.builder import VacationScheduleBuilder
from apps.vacations.schedule.navigation import NavigationService
from apps.common.localization.months import get_month
from apps.vacations.forms import VacationScheduleFilterForm
from apps.common.page import (
    PageAction,
    PageContext,
)


class VacationScheduleView(LoginRequiredMixin, TemplateView):
    """
    Графік відпусток.
    """

    template_name = "vacations/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()

        form = VacationScheduleFilterForm(
            self.request.GET or None,
        )
        if form.is_valid():
            year = form.cleaned_data["year"]
            month = form.cleaned_data["month"]
        else:
            year = form.fields["year"].initial
            month = form.fields["month"].initial

        schedule = VacationScheduleBuilder.build(
            year,
        )
        context["schedule"] = schedule
        context["year"] = year
        context["month"] = month
        context["page"] = PageContext(
            title="Графік відпусток",
            subtitle=f"{get_month(month).nominative} {year}",
            navigation=NavigationService.build(
                year,
                month,
            ),
            actions=[
                PageAction(
                    title="PDF",
                    url="#",
                ),
                PageAction(
                    title="Excel",
                    url="#",
                ),
            ],
            filter_form=form,
        )

        return context
