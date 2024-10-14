""" machines forms"""

from django import forms

from .models import Machine, MachineState


class MachineStateForm(forms.ModelForm):
    """machine state forms"""

    class Meta:
        model = MachineState
        fields = ("name",)
        labels = {
            "name": "Nome da máquina",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class MachineForm(forms.ModelForm):
    """Register machine form"""

    class Meta:
        model = Machine
        fields = [
            "name",
            "state",
            "purchase_value",
            "description",
        ]

    name = forms.CharField(
        label="Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Insira o nome", "class": "form-control"}),
    )

    description = forms.CharField(
        label="Descrição",
        required=True,
        max_length=100,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Descrição",
                "class": "form-control",
                "rows": 1,
                "cols": 40,
                "style": "height: 150px;",
            }
        ),
    )

    purchase_value = forms.DecimalField(
        label="Preço de Compra",
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Insira o preço de compra", "class": "form-control"}),
    )

    state = forms.ModelChoiceField(
        label="Estado da Máquina",
        required=True,
        queryset=MachineState.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
