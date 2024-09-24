from fastapi import Request
from nicegui import ui, APIRouter, app
from constants import DOMAIN, USER_INFO
from pages.components.header import header
from pages.components.user import validate_user_session, add_head_descope_scripts
from pages.components.stripe_elements import stripe_checkout_button


router = APIRouter()

@router.page('/upgrade')
async def upgrade_page():
    features = [
        'AI powered analysis and suggestions',
        'Life time access',
        'Unlimited credits',
        'Get early access to new features',
        '20% goes to nicegui development support'
    ]

    add_head_descope_scripts()
    header()

    user_data = app.storage.user.get(USER_INFO, {})
    def feature(feature_text):
        with ui.element('li').classes('flex items-start') as li1:
            ui.icon('check_circle').classes('text-lg text-green-500')
            with ui.element('p').classes('ml-3 text-sm') as p2:
                ui.label(feature_text)
    
    with ui.element('div').classes('flex flex-col rounded-lg bg-gray-300 mx-auto') as div1:
        with ui.element('div').classes('px-6 py-8 sm:p-10 sm:pb-6') as div2:
            with ui.element('div') as div3:
                with ui.element('span').classes('inline-flex rounded-full bg-violet-100 px-3 py-1 text-sm font-semibold text-violet-600') as span1:
                    ui.label('Standard')
            with ui.element('div').classes('mt-4 flex items-baseline text-6xl font-extrabold') as div4:
                ui.label('$19.99')
                with ui.element('span').classes('ml-4 text-2xl font-medium text-gray-500') as span2:
                    ui.label('single payment')
            with ui.element('p').classes('mt-5 text-lg text-gray-500') as p1:
                ui.label('Life time access to all features with unlimited credits')
            stripe_checkout_button(
                #'price_1PpnOVKGJszy6fxkVRQE42hq', 
                'price_1Py713KGJszy6fxk2Z2aKsQi', 
                f'{DOMAIN}/video', 
                f'{DOMAIN}/video', 
                metadata={'user_id': user_data.get('id'), 'session_id': app.storage.browser['id']} ).classes('w-full p-4 mt-4 text-xl')
        with ui.element('div').classes('flex flex-1 flex-col justify-between rounded-b-lg bg-gray-900 p-6 sm:p-10 sm:pb-6 text-gray-300') as div5:
            with ui.element('ul').classes('space-y-4') as ul:
                for feature_text in features:
                    feature(feature_text)

    await ui.context.client.connected()
    await validate_user_session('/upgrade')

    
