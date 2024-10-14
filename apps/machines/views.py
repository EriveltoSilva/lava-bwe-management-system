"""views for machines """

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MachineForm


class RegisterMachinesView(View):
    """View for register machines"""

    template_name = "machines/register.html"
    form_class = MachineForm

    def get(self, request, *args, **kwargs):
        """registers a machine"""
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "menu_page": "machines", "sub_page": "register"})

    def post(self, request, *args, **kwargs):
        """registers a machine post data"""
        form = self.form_class(request.POST)
        if form.is_valid():
            # save form data
            machine = form.save(commit=False)
            machine.created_by = request.user
            machine.save()
            messages.success(request, "Máquina registada com sucesso!")
        else:
            messages.error(request, "Usuário não encontrado!")

        previous_page = request.META.get("HTTP_REFERER")
        return HttpResponseRedirect(previous_page or "")


register = RegisterMachinesView.as_view()


def dashboard(request):
    return render(request, "home.html")
