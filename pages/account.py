from nicegui import ui, APIRouter, app
from constants import USER_INFO
from pages.components.header import header
from pages.components.user import add_head_descope_scripts, validate_user_session, logout

router = APIRouter()

@router.page('/account')
async def account_page():

    def card_pair(label, value):
        with ui.row().classes('mt-8 bg-blue-500 rounded-lg items-center '):
            ui.label(label).classes('text-base sm:text-xl font-bold bg-blue-700 p-2 rounded-l-lg ')
            ui.label(value).classes('text-base sm:text-xl mr-4')

    add_head_descope_scripts()
    header()
    with ui.element('div').classes('p-16 w-max-4xl mx-auto items-center bg-gray-800 text-gray-200 rounded-lg shadow-lg'):    
        ui.label('Account').classes('text-4xl font-bold text-center')
        user_data = app.storage.user.get(USER_INFO, {})
        credits = user_data.get('credits')
        if user_data.get('plan') == 'paid':
            credits = 'unlimited'
        card_pair('email:', user_data.get('email'))
        card_pair('plan:', user_data.get('plan'))
        card_pair('credits:', credits)
        if user_data.get('plan') != 'paid':
            ui.button('Upgrade', on_click=lambda: ui.navigate.to('/upgrade')).classes('w-full mt-8 mb-8 ').props('color="purple"')
        with ui.element('div').classes('flex w-full justify-end mt-4'):
            ui.button('Log out', on_click=logout)

    await ui.context.client.connected()
    await validate_user_session('/account')
