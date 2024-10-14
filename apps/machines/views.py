"""views for machines """

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from .forms import MachineForm, MachineStateForm
from .models import Machine, MachineState

NUMBER_OF_MACHINE = 15


class RegisterMachineStateView(View):
    """view for RegisterMachine"""

    template_name = "machines/register-state.html"
    form_class = MachineStateForm

    def get(self, request, *args, **kwargs):
        """render form for register new machine state"""
        form = self.form_class(data=request.session.get("machine_state_form_data", None))
        return render(
            request, self.template_name, {"form": form, "menu_page": "machines", "sub_page": "register-state"}
        )

    def post(self, request, *args, **kwargs):
        """post data for register new machine state"""
        request.session["machine_state_form_data"] = request.POST
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Novo estado de Máquina registado com sucesso!")
            del request.session["machine_state_form_data"]
        else:
            messages.error(request, "Formulário com dados inválidos!")

        previous_page = request.META.get("HTTP_REFERER")
        return HttpResponseRedirect(previous_page or "")


register_state = RegisterMachineStateView.as_view()


class DeleteMachineStateView(View):
    """View for delete machines"""

    def get_object(self, *args, **kwargs):
        """get machine object"""
        mid = self.kwargs.get("mid")
        return MachineState.objects.get(mid=mid)

    def post(self, request, *args, **kwargs):
        """delete a machine"""
        try:
            machine_state = self.get_object(*args, **kwargs)
            machine_state.delete()
            messages.success(request, "Estado deletado com sucesso!")
        except MachineState.DoesNotExist as e:
            messages.error(request, f"Estado da Máquina não encontrada: {e}")
        return redirect(request.META.get("HTTP_REFERER") or "")


delete_machine_states = DeleteMachineStateView.as_view()


class ListStateMachine(View):
    """View for list machine states"""

    template_name = "machines/state_list.html"

    def get(self, request, *args, **kwargs):
        """list machines state"""
        list_machine_states = MachineState.objects.all()
        paginator = Paginator(list_machine_states, NUMBER_OF_MACHINE)
        page = request.GET.get("page")
        machine_states = paginator.get_page(page)

        return render(
            request,
            self.template_name,
            {"machine_states": machine_states, "menu_page": "machines", "sub_page": "state_list"},
        )

    def post(self, request, *args, **kwargs):
        state_name = request.POST.get("name")
        MachineState.objects.create(name=state_name)
        messages.success(request, "Novo estado da máquina cadastrado com sucesso!")
        return redirect(reverse("state_list"))


list_states = ListStateMachine.as_view()


def details(request, slug):
    """View for edit machines"""
    if not request.user.is_authenticated:
        return JsonResponse({"status": "Erro. User não autenticado"})
    if request.method == "GET":
        print("Dados")
        machine = get_object_or_404(Machine, slug=slug)
        data = {
            "name": machine.name,
            "description": machine.description,
            "purchase_value": machine.purchase_value,
            "state": machine.state,
            "created_by": machine.created_by,
            "created_at": machine.created_at.strftime("%d/%m/%Y"),
            "updated_at": machine.updated_at.strftime("%d/%m/%Y"),
        }
    else:
        data = {}
    return JsonResponse({"status": "success", "data": data})


class ListMachineView(View):
    """View for list machines"""

    template_name = "machines/list.html"

    def get_filter_machines(self, request):
        """get machines filter by state"""
        state = request.GET.get("state")
        list_machines = Machine.objects.filter(state__name=state) if state else Machine.objects.all()
        return list_machines

    def get(self, request, *args, **kwargs):
        """list machines"""
        number_active_machines = Machine.objects.filter(state__name__icontains="activo").count()
        list_machines = self.get_filter_machines(request)

        total_machines = len(list_machines)

        paginator = Paginator(list_machines, NUMBER_OF_MACHINE)
        page = request.GET.get("page")
        machines = paginator.get_page(page)

        return render(
            request,
            self.template_name,
            {
                "machines": machines,
                "machines_states": MachineState.objects.all(),
                "total_machines": total_machines,
                "number_active_machines": number_active_machines,
                "menu_page": "machines",
                "sub_page": "list",
            },
        )


list_machine = ListMachineView.as_view()


class DeleteMachineView(View):
    """View for delete machines"""

    def get_object(self, *args, **kwargs):
        """get machine object"""
        slug = self.kwargs.get("slug")
        return Machine.objects.get(slug=slug)

    def post(self, request, *args, **kwargs):
        """delete a machine"""
        try:
            machine = self.get_object(*args, **kwargs)
            machine.delete()
            messages.success(request, "Máquina deletada com sucesso!")
        except Machine.DoesNotExist as e:
            messages.error(request, f"Máquina não encontrada: {e}")
        return redirect(request.META.get("HTTP_REFERER") or "")


delete = DeleteMachineView.as_view()


class EditMachineView(View):
    """View for edit machines"""

    template_name = "machines/edit.html"
    form_class = MachineForm

    def get_object(self, *args, **kwargs):
        """get machine object"""
        slug = self.kwargs.get("slug")
        return Machine.objects.get(slug=slug)

    def get(self, request, *args, **kwargs):
        """edit a machine"""
        machine = self.get_object(*args, **kwargs)
        form = self.form_class(data=request.session.get("edit_machine_form_data", None), instance=machine)
        return render(request, self.template_name, {"form": form, "menu_page": "machines", "sub_page": "edit"})

    def post(self, request, *args, **kwargs):
        """edit a machine post data"""
        machine = self.get_object(*args, **kwargs)
        request.session["edit_machine_form_data"] = request.POST
        form = self.form_class(data=request.POST, instance=machine)

        if form.is_valid():
            machine = form.save(commit=False)
            machine.save()
            messages.success(request, "Máquina editada com sucesso!")
            del request.session["edit_machine_form_data"]
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
        form = self.form_class(data=request.session.get("machine_form_data", None))
        return render(request, self.template_name, {"form": form, "menu_page": "machines", "sub_page": "register"})

    def post(self, request, *args, **kwargs):
        """registers a machine post data"""
        request.session["machine_form_data"] = request.POST
        form = self.form_class(request.POST)
        if form.is_valid():
            # save form data
            machine = form.save(commit=False)
            machine.created_by = request.user
            machine.save()
            messages.success(request, "Máquina registada com sucesso!")
            del request.session["machine_form_data"]
        else:
            messages.error(request, "Usuário não encontrado!")

        previous_page = request.META.get("HTTP_REFERER")
        return HttpResponseRedirect(previous_page or "")


register = RegisterMachinesView.as_view()


def dashboard(request):
    """Returns home page"""
    return render(request, "home.html")
