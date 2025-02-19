#!/usr/bin/env python3.11

# type: ignore
from nicegui import ui, app
from functools import partial
import uuid, importlib, env, asyncio
from utils import header, find, styles, section

# This file is the main homepage of the app


# This sets the pages to be accessible from the home-page, depending on whether the user is logged in
def pages():
    about = ("about", "help", f"About {env.APP_NAME}")
    return (
        [
            about,
            ("request", "shopping_cart", "Order Delivery"),
            ("new", "flight_takeoff", "I'm Flying"),
            ("users", "badge", "Profile"),
        ]
        if "logIn" in app.storage.user
        else [
            about,
            ("join", "person_add", "Create Account"),
            ("users", "diversity_3", "Log In"),
        ]
    )


# Here are the functions that get called when navigating to different pages in our website
@ui.page("/")
def main():
    header(env.APP_NAME)
    styles("main")

    # This uses our list to populate a row of buttons for navigating to the pages
    with ui.row():
        for name, icon, desc in pages():
            with ui.card().classes("box"):
                ui.button(icon=icon).props("outline round").classes(
                    "shadow-lg"
                ).on_click(partial(ui.navigate.to, f"/app/{name}"))
                section(desc)


# This allows pages to be created as long as
#   1. They are included in the pages list in this file
#   2. There is a <page-name>.py file in the pages folder that has a show method to display its contents
@ui.page("/app/{page}")
def App(page: str):
    header(find(pages(), page, 2))
    styles("main")

    body = importlib.import_module(f"pages.{page}")
    body.show()


# async def monitor():
#     while True:
#         print(f"The app is running at {env.APP_NAME}!")
#         await asyncio.sleep(1)


# app.on_startup(monitor)

# This makes the web app visible at localhost:8080
ui.run(
    on_air=env.secret("onair token"),
    storage_secret=f"{uuid.uuid4()}",
    favicon="💼",
    show=False,
    port=8081,
)
