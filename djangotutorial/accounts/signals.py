from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)

from django.dispatch import receiver

from .utils import log_event


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):

    log_event(
        request,
        "login",
        user=user,
        details="User logged in"
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):

    log_event(
        request,
        "logout",
        user=user,
        details="User logged out"
    )