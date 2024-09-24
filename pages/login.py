from nicegui import ui, APIRouter

from pages.components import user

router = APIRouter()


@router.page('/login')
async def login():
    user.add_head_descope_scripts()
    user.login_form()
    await ui.context.client.connected()
    await user.validate_user_session('/login')

@router.page('/logout')
async def logout():
    user.add_head_descope_scripts()
    await ui.context.client.connected()
    await user.logout()
    await user.validate_user_session('/logout')