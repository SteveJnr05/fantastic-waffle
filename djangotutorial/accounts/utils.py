import logging

from .models import AuditLog

logger = logging.getLogger("auth_logger")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    return request.META.get("REMOTE_ADDR")


def log_event(request, event_type, user=None, details=""):

    ip = get_client_ip(request)

    logger.info(
        f"{event_type} | "
        f"user={user} | "
        f"ip={ip}"
    )

    AuditLog.objects.create(
        user=user,
        event_type=event_type,
        ip_address=ip,
        details=details,
    )