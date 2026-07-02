from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import log_event
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

# Create your views here.
class LoginView(TemplateView):
    template_name = "registration/login.html"

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):

        response = super().form_valid(form)

        user = self.object

        login(self.request, user)

        log_event(
            self.request,
            "signup",
            user=user,
            details="User registered"
        )

        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

class CustomPasswordResetConfirmView(
    PasswordResetConfirmView
):

    def form_valid(self, form):

        response = super().form_valid(form)

        log_event(
            self.request,
            "password_reset_complete",
            user=self.user,
            details="Password reset completed"
        )

        return response