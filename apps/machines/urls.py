"""accounts urls"""

from django.urls import path

from . import views

app_name = "machines"

urlpatterns = [
    path("nova-maquina/", views.register, name="register"),
    path("editar-maquina/<slug:slug>", views.edit, name="edit"),
    path("deletar-maquina/<slug:slug>", views.delete, name="delete"),
    path("lista-de-maquinas", views.list_machine, name="list"),
    path("detalhes/<slug:slug>", views.details, name="details-json"),
    #
    path("estados-de-maquinas/novo-estado", views.register_state, name="register-state"),
    path("estados-de-maquinas/deletar/<uuid:mid>", views.delete_machine_states, name="delete-state"),
    path("estados-de-maquinas/editar/<uuid:mid>", views.edit_machine_state, name="edit-state"),
    path("estados-de-maquinas", views.list_states, name="list-states"),
]
