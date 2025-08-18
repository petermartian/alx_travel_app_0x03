# listings/services/chapa.py
import uuid
import requests
from django.conf import settings

BASE_URL = "https://api.chapa.co/v1"


def _headers():
    return {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def generate_tx_ref(prefix="booking"):
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def initialize(
    amount,
    currency,
    email,
    first_name,
    last_name,
    tx_ref,
    callback_url=None,
    return_url=None,
    phone_number=None,
    customization=None,
    meta=None,
):
    payload = {
        "amount": str(amount),
        "currency": currency,
        "email": email,
        "first_name": first_name or "",
        "last_name": last_name or "",
        "tx_ref": tx_ref,
    }
    if phone_number:
        payload["phone_number"] = phone_number
    if callback_url:
        payload["callback_url"] = callback_url
    if return_url:
        payload["return_url"] = return_url
    if customization:
        payload["customization"] = customization
    if meta:
        payload["meta"] = meta

    r = requests.post(f"{BASE_URL}/transaction/initialize", json=payload, headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json()


def verify(tx_ref: str):
    r = requests.get(f"{BASE_URL}/transaction/verify/{tx_ref}", headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json()
