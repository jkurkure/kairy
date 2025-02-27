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
                on_click=funcChain(action, dialog.close),
            ).props("fab color=green")

    return dialog


def severe_error_dialog():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Error!").classes("text-h4")
            ui.label(
                "A severe error has occurred. Please try again later or contact support."
            )
            ui.button(
                "Close",
                on_click=funcChain(
                    functools.partial(ui.navigate.to, "/"), dialog.close
                ),
            ).props("fab color=red")

    return dialog
