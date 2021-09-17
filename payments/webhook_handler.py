from django.http import HttpRequest, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
import os
import time

from commissions.models import Commission, WIP


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, commission):
        """Send the user and artists a confirmation email"""
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
                    'static_dir': 'css/base.css' if 'USE_AWS' in os.environ
                                  else 'static/css/base.css',
                    'link_url': HttpRequest.build_absolute_uri(
                        f'/commission/edit/{commission.id}'
                    )
                }),
            "text/html")
        email.send()

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        commission_id = intent.metadata.commission_id

        commission = Commission.objects.get(pk=commission_id)

        wip_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                wip = WIP.objects.get(commission=commission)
                wip_exists = True
                break
            except WIP.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if wip_exists:
            self._send_confirmation_email(commission)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified WIP already in database'),
                status=200)
        else:
            wip = None
            try:
                wip = WIP.objects.create(commission=commission)
            except Exception as e:
                if wip:
                    wip.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(commission)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created wip in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Failed Payment evet received: {event["type"]}',
            status=200)
