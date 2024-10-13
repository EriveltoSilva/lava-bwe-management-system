"""accounts urls"""

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registrar-conta/", views.register, name="register"),
    path("recuperacao-de-palavra-passe/", views.password_reset, name="password-reset"),
    path("alterar-palavra-passe/", views.password_change, name="password-change"),
    # path("controller/", views.account_controller, name="controller"),
]
