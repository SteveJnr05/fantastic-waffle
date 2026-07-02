from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    EVENT_TYPES = [
        ("signup", "Signup"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("password_reset_request", "Password Reset Request"),
        ("password_reset_complete", "Password Reset Complete"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    details = models.TextField(
        blank=True
    )

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.event_type}"