"""apps configuration"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """accounts configuration class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"

    # def ready(self, *args, **kwargs) -> None:
    # from . import signals

    # return super().ready(*args, **kwargs)
