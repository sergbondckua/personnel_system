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


class ReadOnlyInline(admin.TabularInline):
    """
    Базовий readonly Inline.
    """

    extra = 0

    can_delete = False

    show_change_link = True

    classes = ("tab",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
