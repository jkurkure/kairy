from datetime import datetime
import env
from nicegui import ElementFilter, ui
from functools import partial
from utils import (
    styles,
    section,
    header,
    username,
    password,
    phones,
    Form,
    database,
    dateCheck,
    unique,
    fieldType,
)
import uuid
from itertools import chain

registerTypes = [("Phone Number", "phone"), ("Google Accounts", "google")]

formlabel = partial(section, size=120)

if database.getTable("Users") is None:
    database.newTable("Users", "username", "password", "birth", "phone", "country")


def show():
    styles("main")

    ui.label("We're so glad you want to join the family!").classes("text-h5")

    ui.label("How do you wish to register?")

    with ui.row():
        for type, page in registerTypes:
            with ui.card().classes("box").on(
                "click", partial(ui.navigate.to, f"/app/join/{page}")
            ):
                section(type)


# Sub-pages
@ui.page("/app/join/google")
def google():
    header("Create Account")
    section("Under construction!")


@ui.page("/app/join/phone")
def phone():
    header("Create Account")

    setattr(form := Form(), "valid", False)

    with ui.grid(columns=2):
        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Username: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            ui.input(value=username.generate_uname(f"{uuid.uuid4()}", 2)).props(
                "rounded outlined dense"
            )

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Password: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            pword = ui.input(
                password_toggle_button=True,
                value=password.generate_password(f"{uuid.uuid4()}", 14),
            ).props("rounded outlined dense")

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Confirm Password: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            pword_cfm = ui.input(password=True, password_toggle_button=True).props(
                "rounded outlined dense"
            )

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Date of Birth")
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
            formlabel("Phone Number: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            ui.number(placeholder="Without country code").props(
                "rounded outlined dense"
            )

        with ui.element("div").classes("p-2 bg-orange-100"):
            formlabel("Country Code: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            with ui.row():
                formlabel("+", color=0x222)
                ui.number(
                    placeholder="91",
                    on_change=lambda e: result.set_text(phones.where(f"+{e.value}")[0]),
                ).props("rounded outlined dense").style("width: 60%;")
                result = ui.label()

    fields = list(ElementFilter(kind=fieldType))  # type: ignore

    def formValidCheck(_):
        form.valid = pword_cfm.value == pword.value and (False not in [field.value not in [None, ""] for field in fields]) and dateCheck(date.value, allow_yrs=range(datetime.now().year - 100, datetime.now().year - env.MIN_AGE))  # type: ignore

    [field.on("change", formValidCheck) for field in fields]

    def createAccount(e):
        if form.valid:  # type: ignore
            if database.hasCell("Users", "username", fields[0].value):
                ui.notify("That username is taken!")
            else:
                database.addRow("Users", *unique([field.value for field in fields]))
                ui.navigate.to("/app/users")

    ui.button("Create Account").props("rounded outlined").bind_enabled_from(
        form, "valid"
    ).on("click", createAccount)
