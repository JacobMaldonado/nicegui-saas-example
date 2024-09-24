import logging
import os
from typing import Any, Callable, Dict

from descope import AuthException, DescopeClient

from nicegui import app, helpers, ui

from domain.UserManagementUseCase import UserManagementUseCase
from models.User import User
from constants import USER_INFO

DESCOPE_ID = os.environ.get('DESCOPE_PROJECT_ID', '')
SESSION_TOKEN_REFRESH_INTERVAL = 30
LOGIN_PATH = '/login'

try:
    descope_client = DescopeClient(project_id=DESCOPE_ID)
except AuthException as ex:
    print(ex.error_message)

def on_success_login(e) -> None:
    user_data = e.args['detail']['user']
    app.storage.user.update({'descope': user_data})
    userManagementUseCase = UserManagementUseCase()
    user = User(id=user_data['userId'], email=user_data['email'])
    user = userManagementUseCase.login_user(user)
    app.storage.user.update({USER_INFO: user.model_dump()})
    ui.navigate.to('/video')


def login_form() -> ui.element:
    """Create and return the Descope login form."""
    with ui.card().classes('w-96 mx-auto'):
        return ui.element('descope-wc').props(f'project-id="{DESCOPE_ID}" flow-id="sign-up-or-in"') \
            .on('success', on_success_login)


def about() -> Dict[str, Any]:
    """Return the user's Descope profile.

    This function can only be used after the user has logged in.
    """
    return app.storage.user['descope']


async def logout() -> None:
    """Logout the user."""
    result = await ui.run_javascript('return await sdk.logout()')
    if result['code'] == 200:
        app.storage.user['descope'] = {}
        app.storage.user[USER_INFO] = {}
        logging.info('Logged out')
    else:
        logging.error(f'Logout failed: {result}')
        ui.notify('Logout failed', type='negative')
    ui.navigate.to(LOGIN_PATH)

def add_head_descope_scripts() -> None:
        ui.add_head_html('<script src="https://unpkg.com/@descope/web-component@latest/dist/index.js"></script>')
        ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk@latest/dist/index.umd.js"></script>')
        ui.add_body_html(f'''
            <script>
                const sdk = Descope({{ projectId: '{DESCOPE_ID}', persistTokens: true, autoRefresh: true }});
                const sessionToken = sdk.getSessionToken()
            </script>
        ''')

async def validate_user_session(path) -> None:
    if await _is_logged_in():
        if path == LOGIN_PATH:
            #_refresh()
            print(about())
            ui.navigate.to('/video')
            return
        ui.timer(SESSION_TOKEN_REFRESH_INTERVAL, _refresh)
    else:
        if path != LOGIN_PATH:
            ui.navigate.to(LOGIN_PATH)
            return

    
async def _is_logged_in() -> bool:
    if not app.storage.user.get('descope'):
        return False
    token = await ui.run_javascript('return sessionToken && !sdk.isJwtExpired(sessionToken) ? sessionToken : null;')
    if not token:
        return False
    try:
        descope_client.validate_session(session_token=token)
        return True
    except AuthException:
        logging.exception('Could not validate user session.')
        ui.notify('Wrong username or password', type='negative')
        return False

def _refresh() -> None:
    print('Refreshing')
    ui.run_javascript('sdk.refresh()')

