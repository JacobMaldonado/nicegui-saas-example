from nicegui import ui

def showcase(title, description, video_url) -> None:
    ui.link_target('showcase')
    with ui.element('div').classes('mx-auto bg-gray-900 rounded-xl shadow-md overflow-hidden p-6 md:w-full'):
        with ui.element('div').classes('shadow-lg rounded-xl bg-white mx-auto max-w-6xl md:flex md:w-full'):
            with ui.card().classes('md:w-2/5 rounded-xl p-6'):
                    ui.label(title).classes('text-2xl font-bold text-gray-900')
                    ui.label(description).classes('text-base text-gray-600')
            ui.html(f'<iframe src="{video_url}" class="w-full h-full" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>').classes('w-full rounded-lg shadow-lg aspect-video')