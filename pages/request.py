from datetime import datetime
import uuid
from nicegui import ElementFilter, ui
from utils import database, dateCheck, section, fieldType, Form, unique
from .join import formlabel
import env


def show():
    setattr(form := Form(), "valid", False)

    section("Tell us more!")

    with ui.grid(columns=2):
        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Item name: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            ui.input(
                validation=lambda value: (
                    "Only letters in your item's name please"
                    if not value.replace(" ", "").isalpha()
                    else None
                )
            ).props("rounded outlined dense")

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Where do you want it delivered?")
        with ui.element("div").classes("p-2 bg-blue-100"):
            ui.input(autocomplete=["London", "Lucarno"])

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("When do you want it delivered?")
        with ui.element("div").classes("p-2 bg-blue-100"):
            with ui.input("Date") as date:
                with ui.menu().props("no-parent-event") as menu:
                    with ui.date().bind_value(date).on_value_change(
                        lambda e: formValidCheck(e)
                    ):
                        with ui.row().classes("justify-end"):
                            ui.button("Close", on_click=menu.close).props("flat")
                with date.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu.open).classes(
                        "cursor-pointer"
                    )

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("How much are you offering?")
        with ui.element("div").classes("p-2 bg-blue-100"):
            ui.number(min=2.50, max=100, step=0.01, prefix="SG $")

    fields = list(ElementFilter(kind=fieldType))  # type: ignore

    def formValidCheck(_):
        form.valid = (False not in [field.value not in [None, ""] and not (field.validation and field.validation(field.value)) for field in fields]) and dateCheck(date.value, allow_yrs=range(datetime.now().year, datetime.now().year + env.MAX_ADVANCE_YRS + 1))  # type: ignore

    [field.on("change", formValidCheck) for field in fields]

    def listItem(e):
        if form.valid:  # type: ignore
            database.addRow(
                "Items", *unique([uuid.uuid4()] + [field.value for field in fields])
            )
            ui.navigate.to("/app/users")

    ui.button("List").props("rounded outlined").bind_enabled_from(form, "valid").on(
        "click", listItem
    )
