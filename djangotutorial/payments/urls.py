from django.urls import path

from . import views

urlpatterns = [
    path("plans/", views.plans_view, name="plans"),
    path(
        "initialize/<int:plan_id>/",
        views.initialize_payment,
        name="initialize_payment",
    ),
    path(
        "verify/",
        views.verify_payment,
        name="verify_payment",
    ),
    path(
        "webhook/",
        views.paystack_webhook,
        name="paystack_webhook",
    )
]