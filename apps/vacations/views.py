from calendar import monthrange
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.common.utils.dates import month_name
from apps.organization.tree import OrganizationTreeService
from apps.vacations.schedule.calendar import CalendarService
from apps.vacations.schedule_builder import VacationScheduleBuilder
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

        first_day = date(
            year,
            month,
            1,
        )

        last_day = date(
            year,
            month,
            monthrange(year, month)[1],
        )

        tree = OrganizationTreeService.build()

        VacationScheduleBuilder.fill(
            tree,
            first_day,
            last_day,
        )

        context["tree"] = tree

        context["calendar"] = CalendarService.month(
            year,
            month,
        )

        context["year"] = year
        context["month"] = month
        context["month_name"] = month_name(today.month)
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


def get_initial(self):
    initial = super().get_initial()

    if self.request.GET.get("person"):
        initial["person"] = self.request.GET["person"]

    if self.request.GET.get("date_from"):
        initial["date_from"] = self.request.GET["date_from"]
        initial["date_to"] = self.request.GET["date_from"]

    return initial
