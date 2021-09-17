from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from profiles.models import UserProfile
from commissions.models import Commission, WIP

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

    if request.method == 'POST':
        WIP.objects.create(commission=commission)

        artist_users = User.objects.filter(is_superuser=True)

        emails_list = []
        for artist in artist_users:
            emails_list.append(artist.email)

        email = EmailMultiAlternatives(
            subject=render_to_string(
                'payments/confirmation_email/confirmation_email_subject.txt',
                {'commission': commission}),
            body=render_to_string(
                'payments/confirmation_email/confirmation_email_body.txt',
                {'commission': commission}),
            to=[commission.user_profile.user.email],
            bcc=emails_list
        )

        email.attach_alternative(
            render_to_string(
                'payments/confirmation_email/confirmation_email_body.html',
                {
                    'commission': commission,
                    'MEDIA_URL': settings.MEDIA_URL,
                    'link_url': request.build_absolute_uri(
                        f'/commission/edit/{commission_id}'
                    )
                }),
            "text/html")
        email.send()

        return redirect(reverse(
            'payment_success', args=[commission.id]))

    else:
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


@login_required
def payment_success(request, commission_id):
    """
    A view to return the payment success page
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    commission = get_object_or_404(Commission, pk=commission_id)

    if commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    context = {
            'profile': profile,
            'commission': commission,
        }

    return render(request, 'payments/payment_success.html', context)
