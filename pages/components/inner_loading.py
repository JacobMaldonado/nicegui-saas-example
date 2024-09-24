from nicegui import ui

def inner_loading():
    with ui.element('q-inner-loading').props('showing') as loading:
        ui.spinner('dots',size='5em')
        ui.label('loading').classes('text-gray-900 text-center block')
    return loading
