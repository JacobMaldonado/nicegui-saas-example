#!/usr/bin/env python3
import os
from nicegui import ui
from pages.components.svg_image import svg_image


def headline(tag_line, description, primary_button_text, secondary_button_text, primary_button_func, secondary_button_func) -> None:
    ui.link_target('headline')
    with ui.element('div').classes('bg-gray-900 py-20 w-full place-content-center').style('height: 80vh'):
        with ui.element('div').classes('container mx-auto px-6 md:px-12'):
            with ui.element('div').classes('flex flex-col md:flex-row items-center'):
                with ui.element('div').classes('md:w-1/2 lg:w-2/3'):
                    with ui.element('h1').classes('text-4xl md:text-6xl lg:text-7xl text-white font-bold mb-6'):
                        ui.label(tag_line[0])
                        ui.label(tag_line[1]).classes('text-indigo-500')
                        ui.label(tag_line[2])
                    ui.label(description).classes('text-lg md:text-xl lg:text-2xl text-gray-400 mb-8 mr-16')
                    with ui.row():
                        ui.button(primary_button_text, on_click=primary_button_func).classes('bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-3 px-6 rounded-md')
                        ui.button(secondary_button_text, on_click=secondary_button_func).props('outline').classes('bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-md')                
                with ui.element('div').classes('w-2/3 md:w-1/2 lg:w-1/3 mt-8 md:mt-0'):
                    path = os.path.join('pages', 'static', 'undraw_conference_re_2yld.svg')
                    svg_image(path).props().classes('rounded-lg shadow-lg')
                