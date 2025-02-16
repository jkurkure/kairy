#!/usr/bin/env python3.11

# type: ignore
from nicegui import ui, app
from functools import partial 
import uuid, importlib
from utils import header, find, styles, section

# This file is the main homepage of the app

# This sets the pages to be accessible from the home-page, depending on whether the user is logged in
def pages():
    return [
        ("about", "help", "About Kairy"),
        ("request", "shopping_cart", "Order Delivery"),
        ("new", "flight_takeoff", "I'm Flying"),
        ("users", "badge", "Profile")
        ] if 'logIn' in app.storage.user else [
        ("about", "help", "About Kairy"),
        ("join", "person_add", "Create Account"),
        ("users", "diversity_3", "Log In")
    ]

# Here are the functions that get called when navigating to different pages in our website
@ui.page('/')
def main():
    header('Kairy')
    styles('main')

    # This uses our list to populate a row of buttons for navigating to the pages
    with ui.row():
        for name, icon, desc in pages():
            with ui.card().classes('box'):
                ui.button(icon=icon).props('outline round').classes('shadow-lg').on_click(
                    partial(ui.navigate.to, f'/app/{name}')
                )
                section(desc)

# This allows pages to be created as long as
#   1. They are included in the pages list in this file
#   2. There is a <page-name>.py file in the pages folder that has a show method to display its contents
@ui.page('/app/{page}')
def App(page: str):
    header(find(pages(), page, 2))
    styles('main')

    body = importlib.import_module(f'pages.{page}')
    body.show()

# This makes the web app visible at localhost:335
ui.run(port=8135, storage_secret=f'{uuid.uuid4()}', favicon='💼')