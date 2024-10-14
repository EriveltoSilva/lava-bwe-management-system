"""views for machines """

from django.shortcuts import redirect, render
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
            form.save()
            return redirect("machines:dashboard")
        return render(request, self.template_name, {"form": form})


register = RegisterMachinesView.as_view()


def dashboard(request):
    return render(request, "home.html")
