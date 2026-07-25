from django.urls import path

from .views import (
    VacationScheduleView,
    VacationListView,
    VacationDetailView,
    VacationUpdateView,
    VacationCreateView,
)

app_name = "vacations"

urlpatterns = [
    path(
        "schedule/",
        VacationScheduleView.as_view(),
        name="schedule",
    ),
    path(
        "",
        VacationListView.as_view(),
        name="list",
    ),
    path(
        "<int:pk>/",
        VacationDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/edit/",
        VacationUpdateView.as_view(),
        name="update",
    ),
    path(
        "create/",
        VacationCreateView.as_view(),
        name="create",
    ),
]
