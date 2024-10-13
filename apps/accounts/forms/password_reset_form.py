"""password reset form module"""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class PasswordResetForm(forms.Form):
    """password reset form"""

    class Meta:
        model = User
        fields = ["email"]

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        error_messages={"required": "Este campo é obrigatório"},
        widget=forms.EmailInput(attrs={"placeholder": "Seu e-mail", "class": "form-control"}),
    )


class PasswordChangeForm(forms.Form):
    """password change form"""

    class Meta:
        model = User
        fields = ["new_password", "confirmation_password"]

    new_password = forms.CharField(
        label="Nova Palavra-passe",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Nova Palavra-passe", "class": "form-control form-control-lg fs-6"}
        ),
    )

    confirmation_password = forms.CharField(
        label="Confirme a Palavra-Passe",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmação da Nova Palavra-passe", "class": "form-control form-control-lg fs-6"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        password2 = cleaned_data.get("confirmation_password")

        if password != password2:
            raise ValidationError(
                {"password": "Os campos de senha devem ser iguais", "password2": "Os campos de senha devem ser iguais"}
            )
        elif len(password) < 8:
            raise ValidationError(
                {
                    "password": "As senhas devem ter no minimo 8 caracteres",
                    "password2": "As senhas devem ter no minimo 8 caracteres",
                }
            )
