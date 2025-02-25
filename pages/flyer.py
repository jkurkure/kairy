import functools
import importlib
from nicegui import ui

from utils import section
import utils

pages = [
    ("view_items", "list", "View Items"),
    ("add_flight", "flight", "Add Upcoming Flight"),
]


def show():
    with ui.grid(columns=2):
        for name, icon, desc in pages:
            with ui.card().classes("box"):
                ui.button(icon=icon).props("outline round").classes(
                    "shadow-lg"
                ).on_click(functools.partial(ui.navigate.to, f"/app/flyer/{name}"))
                section(desc)


@ui.page("/app/flyer/{subpage}")
def App(subpage: str):
    utils.header(utils.find(pages, subpage, 2))
    utils.styles("main")

    body = importlib.import_module(f"pages.flyersub.{subpage}")
    body.show()
