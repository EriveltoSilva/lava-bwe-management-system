"""accounts views"""

from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

# from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View

# from . import emails, utils
from .forms import LoginForm, RegisterForm

# , PasswordChangeForm, PasswordResetForm, SignupBusinessForm, SignupPersonalForm
from .models import Employee

# # from .forms import LoginForm, PasswordChangeForm, PasswordResetForm, SignupBusinessForm, SignupPersonalForm
User = get_user_model()


class RegisterView(View):
    """register view"""

    form_class = RegisterForm
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        """get template for register"""
        form = self.form_class(request.session.get("register_form_data", None))
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """register post data"""
        request.session["register_form_data"] = request.POST

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.first_name = form.cleaned_data.get("first_name")
            # user.last_name = form.cleaned_data.get("last_name")
            user.set_password(user.password)
            user.save()
            print(form.cleaned_data.get("area"))
            Employee.objects.create(
                bi=form.cleaned_data.get("bi"),
                user=user,
                gender=form.cleaned_data.get("gender"),
                birthday=form.cleaned_data.get("birthday"),
                area=form.cleaned_data.get("area"),
                phone=form.cleaned_data.get("phone"),
                created_by=request.user,
                updated_by=request.user,
            )
            messages.success(request, "Usuário Registado com sucesso!")
            del request.session["register_form_data"]
            return redirect("accounts:login")
        print(form.errors)
        return redirect("accounts:register")


register = RegisterView.as_view()


class LoginView(View):
    """login form view"""

    form_class = LoginForm
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        """get login form"""
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """post login data"""
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email", "")
            user = auth.authenticate(request, email=email, password=form.cleaned_data.get("password", ""))
            if user:
                auth.login(request, user=user)
                messages.success(request, f"Bem-vindo de volta Sr(a).{request.user.get_full_name()}!")
                return redirect(reverse("dashboard"))
            messages.error(request, "Ups! Usuário não Encontrado! Verifique por favor as credencias!")
        else:
            messages.error(request, "Error validando o formulário!")
        return redirect("accounts:login")


login = LoginView.as_view()


# @method_decorator(login_required(login_url="/accounts/login", redirect_field_name="next"), name="dispatch")
class LogoutView(View):
    """logout view"""

    def get_redirect_url(self):
        """return url to go after logout"""
        return redirect(reverse("accounts:login"))

    def get(self, request, *args, **kwargs):
        """logout with get method function"""
        if not request.user.is_authenticated:
            return self.get_redirect_url()

        auth.logout(request)
        messages.success(request, "Logout com sucesso!")
        return self.get_redirect_url()

    def post(self, request, *args, **kwargs):
        """logout with post method function"""
        if not request.user.is_authenticated:
            return self.get_redirect_url()
        auth.logout(request)
        messages.success(request, "Logout com sucesso!")
        return self.get_redirect_url()


logout = LogoutView.as_view()


# class PasswordResetEmailVerifyView(View):
#     form_class = PasswordResetForm
#     template_name = "accounts/password-reset.html"

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(request.session.get("password_reset_form_data", None))
#         return render(request, self.template_name, {"form": form})

#     def post(self, request, *args, **kwargs):
#         request.session["password_reset_form_data"] = request.POST
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             try:
#                 user = get_object_or_404(User, email=form.cleaned_data.get("email"))
#                 user.otp = otp = utils.generate_otp()
#                 user.save()
#                 uidb64 = user.id
#                 link = f"http://localhost:8000/accounts/alterar-palavra-passe?otp={otp}&uidb64={uidb64}"
#                 print("#" * 100)
#                 print(link)
#                 print("#" * 100)
#                 try:
#                     emails.send_password_reset(user, user.email, "EJZ Tecnologia", "", link)
#                 except Exception as e:
#                     print("Error sending email for reset password", e)

#                 del request.session["password_reset_form_data"]
#                 messages.success(request, "Enviamos um email de recuperação de palavra-passe para si!")
#             except:
#                 messages.error(request, "Não temos nenhum usuário vinculado a este e-mail")
#         else:
#             messages.error(request, "Error validando o formulário!")
#         previous_page = request.META.get("HTTP_REFERER")
#         return HttpResponseRedirect(previous_page or "")


# password_reset = PasswordResetEmailVerifyView.as_view()


# class PasswordChangeView(View):
#     form_class = PasswordChangeForm
#     template_name = "accounts/password-change.html"

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {"form": form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = User.objects.get(id=request.GET.get("uidb64"), otp=request.GET.get("otp"))
#             if user:
#                 user.set_password(form.cleaned_data.get("new_password"))
#                 user.otp = ""
#                 user.reset_token = ""
#                 user.save()
#                 messages.success(request, "Palavra-passe alterada com sucesso!")
#                 return redirect("accounts:login")
#         else:
#             messages.error(request, "Error validando o formulário!")
#         previous_page = request.META.get("HTTP_REFERER")
#         return HttpResponseRedirect(previous_page or "")


# password_change = PasswordChangeView.as_view()
