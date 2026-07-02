from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event_type",
        "ip_address",
        "timestamp"
    )

    list_filter = (
        "event_type",
        "timestamp"
    )

    search_fields = (
        "user__username",
    )