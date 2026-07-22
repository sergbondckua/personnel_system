from django.urls import path

from .views import VacationScheduleView

app_name = "vacations"

urlpatterns = [
    path(
        "schedule/",
        VacationScheduleView.as_view(),
        name="schedule",
    ),
]
