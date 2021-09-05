from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from profiles.models import UserProfile
from commissions.models import Commission

import stripe


@login_required
def payment(request, commission_id):
    """
    A view to return the payment page
    with the commission information
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    profile = get_object_or_404(UserProfile, user=request.user)
    commission = get_object_or_404(Commission, pk=commission_id)

    if commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    if hasattr(commission, 'wip'):
        messages.error(
            request, 'This commission is already paid')
        return redirect(reverse('profile'))

    stripe_total = round(commission.order_total*100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        'commission': commission,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'payments/payment.html', context)
