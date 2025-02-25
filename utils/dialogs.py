import functools
from nicegui import ui
from utils import funcChain


def order_success_dialog(action):
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Success!").classes("text-h4")
            ui.label(
                "Success! Your request has been made and has been sent to our flyers. We will keep you updated on any offers made."
            )
            ui.button(
                "Close",
                on_click=funcChain(
                    functools.partial(ui.navigate.to, "/app/users"), dialog.close
                ),
            ).props("fab color=green")

    return dialog
