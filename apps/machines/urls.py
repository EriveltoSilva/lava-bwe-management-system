"""accounts urls"""

from django.urls import path

from . import views

app_name = "machines"

urlpatterns = [
    path("nova-maquina/", views.register, name="register"),
    path("editar-maquina/<slug:slug>", views.edit, name="edit"),
    path("lista-de-maquinas", views.list_machine, name="list"),
    path("detalhes/<slug:slug>", views.details, name="details-json"),
]
