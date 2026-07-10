from django.db import models


class AssignmentQuerySet(models.QuerySet):
    """
    QuerySet для роботи з призначеннями.
    """

    def active(self):
        return self.filter(is_active=True)

    def for_person(self, person):
        return self.filter(person=person)

    def current(self):
        return self.active()

    def for_unit(self, org_unit):
        return self.active().filter(
            staff_position__org_unit=org_unit,
        )


class AssignmentManager(models.Manager):
    """
    Manager для моделі Assignment.
    """

    def get_queryset(self):
        return AssignmentQuerySet(
            self.model,
            using=self._db,
        )

    def active(self):
        return self.get_queryset().active()

    def current(self):
        return self.get_queryset().current()

    def for_person(self, person):
        return self.get_queryset().for_person(person)

    def for_unit(self, org_unit):
        return self.get_queryset().for_unit(org_unit)
