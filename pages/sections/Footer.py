from nicegui import ui

def footer(company_name, resources, support, contact_us, rights_reserved) -> None:
    ui.link_target('footer')
    with ui.element('div').classes('bg-gray-100 w-full'):
        with ui.element('div').classes('max-w-screen-lg px-4 sm:px-6 text-gray-800 sm:grid md:grid-cols-4 sm:grid-cols-2 mx-auto'):
            with ui.element('div').classes('p-5'):
                with ui.element('h3').classes('font-bold text-xl text-indigo-600'):
                    ui.label(company_name)
            with ui.element('div').classes('p-5'):
                with ui.element('div').classes('text-sm uppercase text-indigo-600 font-bold'):
                    ui.label('Resources')
                for resource in resources:
                    with ui.element('a').props(f'href={resource["link"]}').classes('my-3 block'):
                        ui.label(resource['name']).classes('text-teal-600 text-xs p-1')
            with ui.element('div').classes('p-5'):
                with ui.element('div').classes('text-sm uppercase text-indigo-600 font-bold'):
                    ui.label('Support')
                for support_link in support:
                    with ui.element('a').props(f'href="{support_link["link"]}"').classes('my-3 block'):
                        ui.label(support_link['name']).classes('text-teal-600 text-xs p-1')
            with ui.element('div').classes('p-5'):
                with ui.element('div').classes('text-sm uppercase text-indigo-600 font-bold'):
                    ui.label('Contact us')
                for contact_link in contact_us:
                    with ui.element('a').props(f'href="{contact_link["link"]}"').classes('my-3 block'):
                        ui.label(contact_link['name']).classes('text-teal-600 text-xs p-1')
        with ui.element('div').classes('bg-gray-100 pt-2'):
            with ui.element('div').classes('flex pb-5 px-3 m-auto pt-5 border-t text-gray-800 text-sm flex-col max-w-screen-lg items-center'):
                with ui.element('div').classes('md:flex-auto md:flex-row-reverse mt-2 flex-row flex'):
                    ui.label(rights_reserved)