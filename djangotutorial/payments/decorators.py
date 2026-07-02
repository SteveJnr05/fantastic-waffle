from functools import wraps
from django.shortcuts import redirect
from django.utils import timezone
from .models import Subscription

def subscription_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        try:

            subscription = request.user.subscription

        except Subscription.DoesNotExist:

            return redirect("plans")

        if subscription.end_date < timezone.now():

            return redirect("plans")

        if subscription.status != Subscription.Status.ACTIVE:

            return redirect("plans")

        return view_func(request, *args, **kwargs)

    return wrapper