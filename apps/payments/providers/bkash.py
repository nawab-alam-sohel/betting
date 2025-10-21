"""
Simple bKash adapter stub.
Replace the internals with real HTTP calls when you have sandbox credentials.
This module returns predictable fake responses for tests and local development.
"""
import uuid
from datetime import datetime


class BKashError(Exception):
    pass


def get_token():
    """Return a fake access token and expiry."""
    return {
        'access_token': 'fake-bkash-token-' + uuid.uuid4().hex,
        'expires_in': 3600,
    }


def create_payment(amount_cents, intent_id):
    """
    Simulate server-side payment creation with bKash.
    Returns a dict containing a provider_payment_id and a payment_url (if redirect flow).
    """
    provider_payment_id = 'BK-' + uuid.uuid4().hex[:12]
    return {
        'provider_payment_id': provider_payment_id,
        'amount_cents': amount_cents,
        'created_at': datetime.utcnow().isoformat(),
        'payment_url': f'https://bkash.example/pay/{provider_payment_id}',
    }


def verify_webhook(payload, headers):
    """
    In production verify signature/HMAC in headers. Here we accept any payload and return True.
    """
    return True
