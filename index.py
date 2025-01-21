# type: ignore
from nicegui import ui
from rembg import remove 
from PIL import Image
from functools import partial 
import uuid, importlib

# This file is the main homepage of the app


# Here are some helper functions and variables
def header(title):
    ui.page_title('Kairy')
    with ui.header():
        with ui.row().classes('text-h3'):
            ui.label('🏠').on('click', js_handler='''() => {
            window.location.href = '/';
            }''').style('cursor: pointer;')

            ui.label(f'| {title}')

pages = {
    "about": "About Kairy",
    "join": "Create Account"
}

# This loads all of our page logos and removes the background from them
# Standardize as <single-word-page-name>.png
logos = {name:remove(Image.open(f'resources/images/{name}.png')) for name in pages}



# Here are the functions that get called when navigating to different pages in our website
@ui.page('/')
def main():
    header('Kairy')

    # These cards are basically big buttons for different pages
    with ui.row().style('transform: scale(1.5); margin-top: 10%; margin-left: 20%;'):

        for name, desc in pages.items():
            
            # create the navigation card for the page on the homepage
            with ui.card() \
            .on('click', partial(ui.navigate.to, f'/app/{name}')) \
            .style('background-color: lightblue; cursor: pointer;'):
                
                ui.image(logos[name]) \
                .style('pointer-events: none;')
                with ui.card_section():
                    ui.label(desc)

@ui.page('/app/{page}')
def app(page: str):
    header(pages[page])
    body = importlib.import_module(f'pages.{page}')
    body.show()

# This makes the web app visible at localhost:35
ui.run(port=35, storage_secret=f'{uuid.uuid4()}', favicon='💼')