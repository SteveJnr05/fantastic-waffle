import requests

from django.conf import settings
from django.db import transaction
# initialize_payment(user, plan)
# verify_payment(reference)
# create_subscription(user, plan)

def initialize_paystack_payment(user, payment):
    """
    Initialize a Paystack transaction and return the authorization URL.
    """

    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": user.email,
        "amount": int(payment.amount * 100),  # Convert Naira to Kobo
        "reference": payment.transaction_id,
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30,
    )

    data = response.json()

    if not data["status"]:
        raise Exception(data["message"])

    return data["data"]["authorization_url"]

@transaction.atomic
def verify_paystack_payment(reference):
    """
    Verify a Paystack transaction.
    """

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    data = response.json()

    if not data["status"]:
        raise Exception(data["message"])

    return data["data"]

from datetime import timedelta

from django.utils import timezone

from .models import Subscription


def activate_subscription(payment):
    plan = payment.plan

    end_date = timezone.now() + timedelta(days=plan.duration_days)

    subscription, created = Subscription.objects.update_or_create(
        user=payment.user,
        defaults={
            "plan": plan,
            "status": Subscription.Status.ACTIVE,
            "end_date": end_date,
        },
    )

    return subscription