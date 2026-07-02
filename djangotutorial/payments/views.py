from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Plan, Payment, Subscription
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import uuid, hashlib, hmac, json
from .services import initialize_paystack_payment, activate_subscription, verify_paystack_payment
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def plans_view(request):
    plans = Plan.objects.all()

    return render(
        request,
        "payments/plan_list.html",
        {
            "plans": plans
        }
    )

# @login_required
# class PlanView(LoginRequiredMixin, generic.ListView):
#     model = Plan
#     template_name = "payments/plan_list.html"
#     context_object_name = "plans"

#     def get_queryset(self):
#         return Plan.objects.all()
    

@login_required
def initialize_payment(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)

    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=plan.price,
        transaction_id=str(uuid.uuid4()),
    )

    try:
        authorization_url = initialize_paystack_payment(
            request.user,
            payment,
        )

        return redirect(authorization_url)

    except Exception as e:
        messages.error(request, str(e))
        return redirect("plans")

@csrf_exempt
def paystack_webhook(request):

    signature = request.headers.get("X-Paystack-Signature")

    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        request.body,
        hashlib.sha512,
    ).hexdigest()

    if signature != computed_signature:
        return HttpResponse(status=403)

    payload = json.loads(request.body)

    event = payload["event"]

    if event != "charge.success":
        return HttpResponse(status=200)

    data = payload["data"]

    reference = data["reference"]

@login_required
def verify_payment(request):
    reference = request.GET.get("reference")

    if not reference:
        messages.error(request, "Invalid payment reference.")
        return redirect("plans")

    try:
        result = verify_paystack_payment(reference)

        payment = Payment.objects.get(
            transaction_id=reference
        )

        if result["status"] == "success":

            payment = Payment.objects.select_for_update().get(transaction_id=reference)

            messages.success(
                request,
                "Subscription activated successfully."
            )

        else:
            payment.status = Payment.Status.FAILED
            payment.save()

            messages.error(request, "Payment failed.")

    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")

    except Exception as e:
        messages.error(request, str(e))

    return redirect("plans")