""" register form """

import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.accounts.models import Area

from .. import utils

# from django.utils import timezone


User = get_user_model()


def is_email_valid(email: str) -> bool:
    """Função para validar um endereço de email."""
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$"  # Expressão regular para um email válido
    return re.match(regex, email)  # Retorna True se o email corresponder à expressão regular


def add_attr(field, attr_name, attr_val):
    """add a attribute field"""
    existing_attr = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attr} {attr_val}".strip()


def add_placeholder(field, placeholder_val):
    """add a placeholder to field"""
    field.widget.attrs["placeholder"] = f"{placeholder_val}".strip()


class RegisterForm(forms.ModelForm):
    """register form"""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "area",
            "birthday",
            "gender",
            "phone",
            "bi",
            # "image",
            "type",
            # "address",
            "password",
            "confirmation_password",
        ]

    first_name = forms.CharField(
        label="Primeiro Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Seu primeiro nome", "class": "form-control"}),
        error_messages={"required": "O campo primeiro nome não pode estar vazio!"},
    )

    last_name = forms.CharField(
        label="Sobrenome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Seu sobrenome", "class": "form-control"}),
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Seu username", "class": "form-control"}),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        error_messages={"required": "Este campo é obrigatório"},
        widget=forms.EmailInput(attrs={"placeholder": "Seu e-mail", "class": "form-control"}),
    )

    password = forms.CharField(
        label="Senha",
        required=True,
        max_length=32,
        widget=forms.PasswordInput(attrs={"placeholder": "Insira a sua senha", "class": "form-control"}),
    )

    confirmation_password = forms.CharField(
        label="Senha de Confirmação",
        required=True,
        max_length=32,
        widget=forms.PasswordInput(attrs={"placeholder": "Insira a sua senha novamente", "class": "form-control"}),
    )

    area = forms.ModelChoiceField(
        label="Área", required=True, queryset=Area.objects.all(), widget=forms.Select(attrs={"class": "form-select"})
    )

    birthday = forms.DateField(
        label="Data de Nascimento",
        required=True,
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Sua data de nascimento", "class": "form-control"}
        ),
    )

    gender = forms.ChoiceField(
        label="Género", choices=utils.GENDER, widget=forms.Select(attrs={"class": "form-select"})
    )

    type = forms.ChoiceField(
        label="Tipo de Usuário", choices=utils.TYPE_USER, widget=forms.Select(attrs={"class": "form-select"})
    )

    phone = forms.CharField(
        label="Telefone",
        required=True,
        max_length=13,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "placeholder": "Ex:940811141",
                "class": "form-control",
            }
        ),
    )

    bi = forms.CharField(
        label="Nº do Bilhete",
        required=True,
        max_length=14,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nº do Bilhete",
                "class": "form-control",
            }
        ),
    )

    # address = forms.CharField(
    #     label="Endereço",
    #     required=True,
    #     max_length=255,
    #     widget=forms.TextInput(attrs={"placeholder": "Endereço", "class": "form-control", "size": "w-100"}),
    # )

    def clean_first_name(self):
        """clean the first name"""
        return self.cleaned_data.get("first_name").strip()

    def clean_last_name(self):
        """clean last name"""
        return self.cleaned_data.get("last_name").strip()

    def clean_email(self):
        """clean e-mail"""
        email = self.cleaned_data.get("email").strip()
        if not is_email_valid(email):
            raise ValidationError("Este email é inválido", code="invalid")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário com este email", code="invalid")
        return email

    def clean_username(self):
        """clean username"""
        data = self.cleaned_data.get("username").strip()
        if " " in data:
            raise ValidationError("O username não pode conter espaços em branco", code="invalid")
        return data

    def clean_bi(self):
        """clean bi value"""
        bi = self.cleaned_data.get("bi").strip()
        if len(bi) != 14:
            raise ValidationError("O número de identificação deve ter 14 caracteres.")
        return bi

    def clean_phone(self):
        """clean phone number"""
        phone = self.cleaned_data.get("phone").strip()
        if phone:
            if "+244" not in phone:
                phone = "+244" + phone
            if not re.match(r"^\+244\d{9}$", phone):
                raise ValidationError("O número de telefone deve conter 9 digitos.")
        return phone

    def clean(self):
        """clean data"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation_password = cleaned_data.get("confirmation_password")

        if password != confirmation_password:
            raise ValidationError(
                {
                    "password": "Os campos de senha devem ser iguais",
                    "confirmation_password": "Os campos de senha devem ser iguais",
                }
            )
        elif len(password) < 8:
            raise ValidationError(
                {
                    "password": "As senhas devem ter no minimo 8 caracteres",
                    "confirmation_password": "As senhas devem ter no minimo 8 caracteres",
                }
            )
