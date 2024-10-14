"""views for machines """

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .forms import MachineForm
from .models import Machine, MachineState

NUMBER_OF_MACHINE = 15


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
        form = self.form_class(data=request.session.get("machine_form_data", None), instance=machine)
        return render(request, self.template_name, {"form": form, "menu_page": "machines", "sub_page": "edit"})

    def post(self, request, *args, **kwargs):
        """edit a machine post data"""
        machine = self.get_object(*args, **kwargs)
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
    """Returns home page"""
    return render(request, "home.html")
