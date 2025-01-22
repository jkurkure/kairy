# type: ignore
from nicegui import ui
from functools import partial 
import uuid, importlib
from utils import header, find

# This file is the main homepage of the app

# List of pages, with their icons and descriptions
# Find the full list of possible icons with their names at https://fonts.google.com/icons
pages = [
    ("about", "help", "About Kairy"),
    ("join", "person_add", "Create Account"),
    ("users", "diversity_3", "User Directory")
]


# Here are the functions that get called when navigating to different pages in our website
@ui.page('/')
def main():
    header('Kairy')

    # This is how we add custom CSS (or any other header HTML) to the webpage
    ui.add_head_html('''
        <style type="text/tailwindcss">
            @layer components {
                .box {
                    @apply bg-orange-100 p-12 text-center shadow-lg rounded-lg text-white;
                }
            }
        </style>
    ''')

    # This uses our list to populate a row of buttons for navigating to the pages
    with ui.row():
        for name, icon, desc in pages:
            with ui.card().classes('box'):
                ui.button(icon=icon).props('outline round').classes('shadow-lg').on_click(
                    partial(ui.navigate.to, f'/app/{name}')
                )
                ui.label(desc).style('color: #6E93D6; font-size: 200%; font-weight: 300')

# This allows pages to be created as long as
#   1. They are included in the pages list in this file
#   2. There is a <page-name>.py file in the pages folder that has a show method to display its contents
@ui.page('/app/{page}')
def app(page: str):
    header(find(pages, page, 2))
    body = importlib.import_module(f'pages.{page}')
    body.show()

# This makes the web app visible at localhost:35
ui.run(port=35, storage_secret=f'{uuid.uuid4()}', favicon='💼')