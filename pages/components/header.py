import os
from nicegui import ui, app
from constants import USER_INFO

def header():
    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.html('<a href="https://www.producthunt.com/posts/confidentier?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-confidentier" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=488539&theme=light" alt="Confidentier - Sharpen&#0032;your&#0032;presentation&#0032;skills | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>')
    print("store",app.storage.user.get(USER_INFO, {}))
    with ui.header().classes(remove='nicegui-header').classes('bg-gray-900 h-16'):
        with ui.element('div').classes('flex justify-between items-center h-full px-4'):
            with ui.link().props('href="/video"').classes('h-full w-60'):
                path = os.path.join('pages', 'static', 'logo.jpeg')
                ui.image(source=path).classes('h-full w-60 object-cover').props('fit="fill"')
            if app.storage.user.get(USER_INFO, {}).get('plan') != 'paid':
                with ui.element('div').classes('text-center'):
                    ui.label('Credits')
                    ui.label(app.storage.user.get(USER_INFO, {}).get('credits'))
            with ui.button(icon='menu').props('flat'):
                with ui.menu() as menu:
                    ui.menu_item('Home', lambda: ui.navigate.to('/video'))
                    ui.menu_item('Account', lambda: ui.navigate.to('/account'))
                    if app.storage.user.get(USER_INFO, {}).get('plan') != 'paid':
                        ui.menu_item('Upgrade', lambda: ui.navigate.to('/upgrade'))
                    ui.menu_item('Log out', lambda: ui.navigate.to('/logout'))
            