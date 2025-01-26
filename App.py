# type: ignore
from nicegui import ui
from functools import partial 
import uuid, importlib
from utils import header, find, styles, section

# This file is the main homepage of the app

# List of pages, with their icons and descriptions
# Find the full list of possible icons with their names at https://fonts.google.com/icons
pages = [
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
        for name, icon, desc in pages:
            with ui.card().classes('box'):
                ui.button(icon=icon).props('outline round').classes('shadow-lg').on_click(
                    partial(ui.navigate.to, f'/app/{name}')
                )
                section(desc)

# This allows pages to be created as long as
#   1. They are included in the pages list in this file
#   2. There is a <page-name>.py file in the pages folder that has a show method to display its contents
@ui.page('/app/{page}')
def app(page: str):
    header(find(pages, page, 2))
    body = importlib.import_module(f'pages.{page}')
    body.show()

# This makes the web app visible at localhost:335
ui.run(port=335, storage_secret=f'{uuid.uuid4()}', favicon='💼')