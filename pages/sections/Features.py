from nicegui import ui

def features(title, features_data) -> None:
    ui.link_target('features')
    with ui.element('section').classes('py-12 bg-gray-900 text-gray-100 sm:py-12 lg:py-16 w-full'):
        with ui.element('div').classes('px-4 mx-auto max-w-7xl sm:px-6 lg:px-8'):
            with ui.element('div').classes('max-w-xl mx-auto text-center xl:max-w-2xl'):
                with ui.element('h2').classes('text-3xl font-bold leading-tight text-gray-50 sm:text-4xl xl:text-5xl mb-6'):
                    ui.label(title)
                # with ui.element('p').classes('mb-4'):
                #     ui.label("We are creating a tool that helps you be more productive and efficient when building websites and webapps")
            with ui.element('div').classes('grid max-w-4xl lg:max-w-6xl grid-cols-1 mx-auto mt-8 text-center gap-y-4 sm:gap-x-8 sm:grid-cols-2 lg:grid-cols-3 sm:mt-12 lg:mt-20 sm:text-left'):
                for value in features_data:
                    with ui.card().classes('bg-white shadow-lg rounded-xl p-6'):
                        ui.icon(value['icon']).classes('text-4xl text-gray-900')
                        ui.label(value['title']).classes('text-2xl font-bold text-gray-900')
                        ui.label(value['description']).classes('text-base text-gray-600')
            