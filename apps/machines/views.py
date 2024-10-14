"""views for machines """

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MachineForm
from .models import Machine


class EditMachineView(View):
    """View for edit machines"""

    template_name = "machines/edit.html"
    form_class = MachineForm

    def get(self, request, *args, **kwargs):
        """edit a machine"""
        slug = self.request.kwargs.get("slug")
        machine = Machine.objects.get(slug=slug)
        form = self.form_class(data=request.session.get("machine_form_data", None), instance=machine)
        return render(request, self.template_name, {"form": form, "menu_page": "machines", "sub_page": "edit"})

    def post(self, request, *args, **kwargs):
        """edit a machine post data"""
        slug = self.kwargs.get("slug")
        machine = Machine.objects.get(slug=slug)
        request.session["machine_form_data"] = request.POST
        form = self.form_class(data=request.POST, instance=machine)

        if form.is_valid():
            machine = form.save(commit=False)
            machine.save()
            messages.success(request, "Máquina editada com sucesso!")
            del request.session["machine_form_data"]
        else:
            messages.error(request, "Erro ao editar a máquina!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "")


edit = EditMachineView.as_view()


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
