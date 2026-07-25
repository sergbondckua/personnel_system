from calendar import monthrange
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from apps.common.utils.dates import month_name
from apps.organization.tree import OrganizationTreeService
from apps.vacations.models import Vacation
from apps.vacations.schedule.calendar import CalendarService
from apps.vacations.schedule_builder import VacationScheduleBuilder
from apps.vacations.schedule.navigation import NavigationService
from apps.common.localization.months import get_month
from apps.vacations.forms import VacationScheduleFilterForm
from apps.common.page import (
    PageAction,
    PageContext,
)
from apps.vacations.selectors_list import VacationListSelector
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView

from apps.vacations.forms import VacationForm


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


class VacationListView(LoginRequiredMixin, ListView):
    model = Vacation
    template_name = "vacations/list.html"
    context_object_name = "vacations"

    def get_queryset(self):
        return VacationListSelector.all()


class VacationDetailView(LoginRequiredMixin, DetailView):
    model = Vacation

    template_name = "vacations/detail.html"

    context_object_name = "vacation"


class VacationUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacation

    form_class = VacationForm

    template_name = "vacations/form.html"

    def get_success_url(self):
        return reverse_lazy(
            "vacations:detail",
            kwargs={"pk": self.object.pk},
        )


class VacationCreateView(LoginRequiredMixin, CreateView):
    model = Vacation

    form_class = VacationForm

    template_name = "vacations/form.html"

    def get_initial(self):
        initial = super().get_initial()

        person = self.request.GET.get("person")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        if person:
            initial["person"] = person

        if date_from:
            initial["date_from"] = date_from

        if date_to:
            initial["date_to"] = date_to
        elif date_from:
            initial["date_to"] = date_from

        return initial

    def get_success_url(self):
        return reverse(
            "vacations:detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


def get_initial(self):
    initial = super().get_initial()

    if self.request.GET.get("person"):
        initial["person"] = self.request.GET["person"]

    if self.request.GET.get("date_from"):
        initial["date_from"] = self.request.GET["date_from"]
        initial["date_to"] = self.request.GET["date_from"]

    return initial
