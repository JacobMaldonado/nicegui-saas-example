import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.routing import APIRouter
from nicegui import app
import stripe
from stripe.error import SignatureVerificationError

from constants import USER_INFO
from domain.UserManagementUseCase import UserManagementUseCase


router = APIRouter()    

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        print("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    if event["type"] == "checkout.session.completed":
        print("Checkout session completed")
        user_management_use_case = UserManagementUseCase()
        _object = event.get("data", {}).get("object", {})
        print(_object)
        user_id = _object.get("metadata", {}).get("user_id")
        user = user_management_use_case.upgrade_plan(user_id, 'paid')
        session_id = _object.get("metadata", {}).get("session_id")
        if session_id in app.storage._users:
            app.storage._users[session_id][USER_INFO] = user.model_dump()
    elif event["type"] == "checkout.session.cancelled":
        print("Checkout session cancelled")
    elif event["type"] == "checkout.session.accepted":
        print("Checkout session accepted")
    elif event["type"] == "checkout.session.pending":
        print("Checkout session pending")
    return {}