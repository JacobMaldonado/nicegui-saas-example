import json
import os
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.routing import APIRouter
from nicegui import app
import stripe
from stripe.error import SignatureVerificationError

from constants import USER_INFO
from domain.UserManagementUseCase import UserManagementUseCase


router = APIRouter()    

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None, alias="stripe-signature")):
    payload = await request.body()
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, webhook_secret
        )
    except ValueError as e:
        print("Invalid payload received")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        print("Invalid signature received")
        raise HTTPException(status_code=400, detail="Invalid signature")
    if event["type"] == "checkout.session.completed":
        print("Checkout session completed")
        user_management_use_case = UserManagementUseCase()
        _object = event.get("data", {}).get("object", {})
        print(_object)
        user_id = _object.get("metadata", {}).get("user_id")
        if not user_id:
            print("Missing user_id in metadata")
            return {}
        user = user_management_use_case.upgrade_plan(user_id, 'paid')
        # Note: Session storage updates should be handled through the app storage API
        # The session will be updated when the user next authenticates
    elif event["type"] == "checkout.session.cancelled":
        print("Checkout session cancelled")
    elif event["type"] == "checkout.session.accepted":
        print("Checkout session accepted")
    elif event["type"] == "checkout.session.pending":
        print("Checkout session pending")
    return {}