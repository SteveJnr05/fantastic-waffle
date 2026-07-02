from django.urls import path
from .views import SignUpView, DashboardView, PasswordResetConfirmView, CustomPasswordResetConfirmView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("password_reset/", PasswordResetConfirmView.as_view(), name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]