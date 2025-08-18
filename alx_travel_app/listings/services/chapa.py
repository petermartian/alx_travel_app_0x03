import uuid
import requests
from django.conf import settings
from requests.exceptions import RequestException

BASE_URL = "https://api.chapa.co/v1"

def _headers():
    """Generate headers for Chapa API requests."""
    key = (settings.CHAPA_SECRET_KEY or "").strip()
    if not key:
        raise ValueError(
            "CHAPA_SECRET_KEY is missing. Add it to .env file, e.g.,\n"
            "CHAPA_SECRET_KEY=CHASECK_TEST-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )
    if not key.startswith(("CHASECK_", "CHASECK-")):
        raise ValueError(
            "CHAPA_SECRET_KEY must start with 'CHASECK_' (secret key), "
            "not 'CHPK_' (public key)."
        )
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

def generate_tx_ref(prefix="booking"):
    """Generate a unique transaction reference."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"

def _raise_with_body(resp: requests.Response):
    """Raise HTTPError with response body for debugging."""
    try:
        body = resp.json()
    except ValueError:
        body = resp.text
    msg = f"HTTP {resp.status_code} {resp.reason} for {resp.url}: {body}"
    raise requests.HTTPError(msg, response=resp)

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
    """Initialize a Chapa payment transaction."""
    if not tx_ref:
        raise ValueError("tx_ref is required")
    if not amount or float(amount) <= 0:
        raise ValueError("Amount must be a positive number")
    if not email:
        raise ValueError("Email is required")
    if not currency:
        currency = "ETB"  # Default to ETB for sandbox

    payload = {
        "amount": str(float(amount)),  # Ensure string for API
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

    try:
        response = requests.post(
            f"{BASE_URL}/transaction/initialize",
            json=payload,
            headers=_headers(),
            timeout=30,
        )
        if not response.ok:
            _raise_with_body(response)
        return response.json()
    except RequestException as e:
        raise RequestException(f"Failed to initialize payment: {str(e)}")

def verify(tx_ref: str):
    """Verify a Chapa payment transaction."""
    if not tx_ref:
        raise ValueError("tx_ref is required")
    try:
        response = requests.get(
            f"{BASE_URL}/transaction/verify/{tx_ref}",
            headers=_headers(),
            timeout=30,
        )
        if not response.ok:
            _raise_with_body(response)
        return response.json()
    except RequestException as e:
        raise RequestException(f"Failed to verify payment: {str(e)}")