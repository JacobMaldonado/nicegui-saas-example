import os
import uuid
from fastapi import FastAPI
from nicegui import ui, app
import uvicorn
from pages.landing import router as landing_router
from pages.login import router as login_router
from pages.video_page import router as video_router
from pages.preview_page import router as preview_router
from pages.account import router as account_router
from pages.upgrade import router as upgrade_router
from api.stripe_endpoints import router as stripe_router

from dotenv import load_dotenv, find_dotenv

# Env Variables
load_dotenv(find_dotenv())

# API Fastapi
app.include_router(stripe_router)

# Nicegui Pages
app.include_router(landing_router)
app.include_router(login_router)
app.include_router(video_router)
app.include_router(preview_router)
app.include_router(account_router)
app.include_router(upgrade_router)

icon_path = os.path.join('pages', 'static', 'logo_2.jpeg')
ui.run(title='Confidentier', favicon=icon_path, storage_secret="my_secret_key_2")
