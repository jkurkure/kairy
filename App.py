#!/usr/bin/env python3.11

# type: ignore
import nicegui
import functools
import uuid, importlib, env
import utils

# This file is the main homepage of the app

# This sets the pages to be accessible from the home-page, depending on whether the user is logged in
def get_main_pages():
    about = ("about", "help", f"About {env.APP_NAME}")
    return (
        [
            about,
            ("request", "shopping_cart", "Request Delivery"),
            ("flyer", "flight_takeoff", "I'm Flying"),
            ("users", "badge", "Profile"),
        ]
        if "logIn" in nicegui.app.storage.user
        else [
            about,
            ("join", "person_add", "Create Account"),
            ("users", "diversity_3", "Log In"),
        ]
    )

# Generic function to create navigation buttons for any list of pages
def create_navigation_buttons(pages_list, base_path="/app"):
    with nicegui.ui.row():
        for name, icon, desc in pages_list:
            with nicegui.ui.card().classes("box"):
                nicegui.ui.button(icon=icon).props("outline round").classes(
                    "shadow-lg"
                ).on_click(functools.partial(nicegui.ui.navigate.to, f"{base_path}/{name}"))
                utils.section(desc)

# Generic function to load and display a subpage
def load_subpage(page_path, page_name, pages_list=None):
    if pages_list:
        title = utils.find(pages_list, page_name, 2)
    else:
        title = page_name
    
    utils.header(title)
    utils.styles("main")

    body = importlib.import_module(f"pages.{page_path}")
    body.show()

# Here are the functions that get called when navigating to different pages in our website
@nicegui.ui.page("/")
def main():
    utils.header(env.APP_NAME)
    utils.styles("main")

    # This uses our list to populate a row of buttons for navigating to the pages
    create_navigation_buttons(get_main_pages())

# This allows pages to be created as long as
#   1. They are included in the pages list in this file
#   2. There is a <page-name>.py file in the pages folder that has a show method to display its contents
@nicegui.ui.page("/app/{page}")
def App(page: str):
    load_subpage(page, page, get_main_pages())

# This makes the web app visible at localhost:8080
nicegui.ui.run(
    on_air=env.secret("onair token"),
    storage_secret=f"{uuid.uuid4()}",
    favicon="💼",
    show=False,
    port=8081,
)