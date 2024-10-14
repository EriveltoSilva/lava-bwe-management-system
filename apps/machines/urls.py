"""accounts urls"""

from django.urls import path

from . import views

app_name = "machines"

urlpatterns = [
    path("nova-maquina/", views.register, name="register"),
    path("editar-maquina/<slug:slug>", views.edit, name="edit"),
]
