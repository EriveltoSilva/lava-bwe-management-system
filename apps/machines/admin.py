"""machine administration"""

from django.contrib import admin

from .models import Machine, MachineState


class MachineStateAdmin(admin.ModelAdmin):
    """machine state admin"""

    list_display = ("id", "name", "created_at", "updated_at")
    list_display_links = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    list_per_page = 25


class MachineAdmin(admin.ModelAdmin):
    """machine admin"""

    list_display = ("id", "name", "slug", "purchase_value", "state", "created_at", "updated_at")
    list_display_links = ("id", "name", "slug", "purchase_value", "state", "created_at", "updated_at")
    list_filter = (
        "name",
        "slug",
        "purchase_value",
        "state",
    )
    search_fields = (
        "name",
        "slug",
        "purchase_value",
        "state",
    )
    list_per_page = 25


admin.site.register(Machine, MachineAdmin)
admin.site.register(MachineState, MachineStateAdmin)
