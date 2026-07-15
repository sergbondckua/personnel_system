from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Базовий клас адміністративної панелі.
    """

    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 25
    save_on_top = True
    save_as = True
    show_full_result_count = True

    fieldsets = (
        (
            "Системна інформація",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
