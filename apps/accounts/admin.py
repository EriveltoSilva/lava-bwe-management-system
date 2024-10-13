"""admin account"""

from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Area, Employee

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """user admin"""

    list_display_links = list_display = [
        "first_name",
        "last_name",
        "email",
        "username",
        "is_superuser",
    ]
    search_fields = [
        "email",
        "username",
        "first_name",
        "last_name",
    ]
    list_per_page = 25


admin.site.register(User, UserAdmin)


class AreaAdmin(admin.ModelAdmin):
    """area admin"""

    list_display = ["name", "created_at", "created_by"]
    list_display_links = [
        "name",
    ]
    list_per_page = 25
    list_filter = [
        "name",
    ]
    list_per_page = 25


class EmployeeAdmin(admin.ModelAdmin):
    """Employee admin"""

    list_display = [
        "get_user",
        "gender",
        "birthday",
        "area",
    ]
    list_display_links = [
        "get_user",
        "gender",
        "birthday",
        "area",
    ]
    list_per_page = 25
    list_filter = [
        "area",
    ]
    list_per_page = 25

    def get_user(self, obj):
        """get user name for Employee admin"""
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user.short_description = "Nome do Usuario"


admin.site.register(Area, AreaAdmin)
admin.site.register(Employee, EmployeeAdmin)
