"""login form"""

from django import forms


class LoginForm(forms.Form):
    """login form"""

    email = forms.CharField(
        label="E-mail",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "E-mail", "class": "form-control", "id": "floatingInput"}),
    )

    password = forms.CharField(
        label="Palavra-passe",
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Insira a sua senha", "class": "form-control", "id": "floatingPassword"}
        ),
    )
