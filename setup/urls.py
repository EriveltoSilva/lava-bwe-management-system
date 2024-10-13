""" Global url project """

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.machines import views as views_machines

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views_machines.dashboard, name="dashboard"),
    path("accounts/", include("apps.accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
