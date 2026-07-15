from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.common.admin import BaseAdmin
from apps.personnel.models import Person


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    """
    Адміністрування військовослужбовців.
    """

    list_display = (
        "service_number",
        "full_name",
        "military_rank",
        "military_specialty",
        "personnel_category",
        "is_active",
    )

    list_editable = ("is_active",)

    list_display_links = (
        "service_number",
        "full_name",
    )

    search_fields = (
        "service_number",
        "last_name",
        "first_name",
        "middle_name",
    )

    list_filter = (
        "is_active",
        "military_rank",
        "military_specialty",
        "personnel_category",
    )

    ordering = (
        "last_name",
        "first_name",
        "middle_name",
    )

    autocomplete_fields = (
        "military_rank",
        "military_specialty",
        "personnel_category",
    )

    readonly_fields = BaseAdmin.readonly_fields + ("photo_preview",)

    list_select_related = (
        "military_rank",
        "military_specialty",
        "personnel_category",
    )

    fieldsets = (
        (
            "Основні дані",
            {
                "fields": (
                    "photo_preview",
                    "photo",
                    "service_number",
                    "last_name",
                    "first_name",
                    "middle_name",
                    "birth_date",
                    "sex",
                )
            },
        ),
        (
            "Військовий облік",
            {
                "fields": (
                    "military_rank",
                    "military_specialty",
                    "personnel_category",
                )
            },
        ),
        (
            "Контактна інформація",
            {
                "fields": (
                    "phone",
                    "email",
                )
            },
        ),
        (
            "Додаткова інформація",
            {
                "fields": (
                    "notes",
                    "is_active",
                )
            },
        ),
    ) + BaseAdmin.fieldsets

    @admin.display(description="ПІБ")
    def full_name(self, obj: Person) -> str:
        return obj.full_name

    @admin.display(description="Фото")
    def photo_preview(self, obj: Person) -> str:
        """
        Попередній перегляд фотографії.
        """
        if not obj.photo:
            return "—"

        if photo := obj.photo:
            return mark_safe(
                f'<a href="{photo.url}" target="_blank">'
                f'<img src="{photo.url}" height="320" width="auto" alt="img"></a>'
            )
        return "-"
