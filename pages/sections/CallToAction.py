from typing import List
from nicegui import ui
from pydantic import BaseModel

class PricingCard(BaseModel):
    plan_name: str
    price: str
    price_periodicity: str
    price_description: str
    features: List[str]
    button_text: str
    button_link: str



def call_to_action(description, cards: List[PricingCard], call_to_action_title, call_to_action_description, call_to_action_link) -> None:
    ui.link_target('call-to-action')
    with ui.element('div').classes("mx-auto text-stone-50 mb-24"):
        with ui.element('div'):
            ui.label('Pricing').classes("text-3xl font-bold tracki text-center mt-12 sm:text-5xl ")
            ui.label(description).classes("max-w-3xl mx-auto mt-4 text-xl text-center ")
        
        with ui.element('div').classes("mt-24 container space-y-12 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-x-8"):
            with ui.element('div').classes("relative p-8  border border-gray-200 rounded-2xl shadow-sm flex flex-col"):
                with ui.element('div').classes("flex-1"):
                    ui.label(cards[0].plan_name).classes("text-xl font-semibold ")
                    with ui.element('p').classes("mt-4 flex items-baseline "):
                        ui.label(cards[0].price).classes("text-5xl font-extrabold tracking-tight")
                        ui.label(f'/{cards[0].price_periodicity}').classes("ml-1 text-xl font-semibold")
                    ui.label(cards[0].price_description)
                    with ui.element('ul').classes("mt-6 space-y-5"):
                        for feature in cards[0].features:
                            with ui.element('li').classes("flex"):
                                ui.icon('check').classes("flex-shrink-0 w-6 h-6 text-emerald-50 text-xl ")
                                ui.label(feature).classes("ml-3 mt-1")     
                with ui.element('a').props(f'href={cards[0].button_link}'):
                    ui.label(cards[0].button_text).classes("bg-emerald-50 text-emerald-700 hover:bg-emerald-100 mt-8 block w-full py-3 px-6 border border-transparent rounded-md text-center font-medium")
            for card in cards[1:]:
                with ui.element('div').classes("relative p-8  border border-gray-200 rounded-2xl shadow-sm flex flex-col"):
                    with ui.element('div').classes("flex-1"):
                        ui.label(card.plan_name).classes("text-xl font-semibold ")
                        ui.label('Most popular').classes("absolute top-0 py-1.5 px-4 bg-emerald-500 text-white rounded-full text-xs font-semibold uppercase tracking-wide  transform -translate-y-1/2")
                        with ui.element('p').classes("mt-4 flex items-baseline "):
                            ui.label(card.price).classes("text-5xl font-extrabold tracking-tight")
                            ui.label(f'/{card.price_periodicity}').classes("ml-1 text-xl font-semibold")
                        ui.label(card.price_description)
                        with ui.element('ul').classes("mt-6 space-y-5"):
                            for feature in card.features:
                                with ui.element('li').classes("flex"):
                                    ui.icon('check').classes("flex-shrink-0 w-6 h-6 text-emerald-50 text-xl ")
                                    ui.label(feature).classes("ml-3 mt-1")     
                    with ui.element('a').props(f'href={card.button_link}'):
                        ui.label(card.button_text).classes("bg-emerald-500 text-white  hover:bg-emerald-600 mt-8 block w-full py-3 px-6 border border-transparent rounded-md text-center font-medium")
            
        with ui.element('div').classes("text-center sm:text-left mt-40 mb-20"):
            with ui.element('div').classes("max-w-screen-xl mx-auto text-center py-12 px-4 sm:px-6 lg:py-16 lg:px-8"):
                ui.label(call_to_action_title).classes("text-3xl leading-9 font-extrabold tracking-tight text-white sm:text-4xl sm:leading-10")
                ui.label(call_to_action_description).classes("mt-4")
                with ui.element('div').classes("mt-8 flex justify-center"):
                    with ui.element('div').classes("inline-flex rounded-md shadow"):
                        with ui.element('a').props(f'href={call_to_action_link}'):
                            ui.label('Get started').classes("inline-flex items-center justify-center px-5 py-3 border border-transparent text-base leading-6 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-500 focus:outline-none focus:shadow-outline transition duration-150 ease-in-out")