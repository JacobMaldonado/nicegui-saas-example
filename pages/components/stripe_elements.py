
from contextlib import contextmanager
import os
import stripe
from nicegui import ui

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def stripe_checkout_session(price_id: str, success_url: str, cancel_url: str, metadata: dict = {}):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
    except Exception as e:
        print(f"payment failed {str(e)}")
        return None
    return checkout_session.url


def stripe_checkout_button(price_id: str, success_url: str, cancel_url: str, metadata: dict = {}):
    def handle_click():
        result = stripe_checkout_session(price_id, success_url, cancel_url, metadata)
        if result:
            ui.navigate.to(result)
        else:
            ui.notification("Payment failed", type="negative")
    return ui.button("Buy", on_click=lambda: handle_click())
    

