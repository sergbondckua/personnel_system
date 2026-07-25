from apps.vacations.models import Vacation


class VacationListSelector:
    @staticmethod
    def all():
        return Vacation.objects.select_related(
            "person",
            "vacation_type",
        ).order_by(
            "-date_from",
        )
