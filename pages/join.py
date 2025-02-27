from datetime import datetime
import env
from nicegui import ui
from functools import partial
from utils import (
    header,
    section,
    styles,
    username,
    password,
    phones,
    database,
    unique,
)
import uuid
from utils.forms import (
    Form,
    create_form_label,
    create_date_input,
    get_form_fields,
    setup_validation,
    create_form_row,
)

registerTypes = [("Phone Number", "phone"), ("Google Accounts", "google")]

# Alias for backward compatibility
formlabel = create_form_label

if database.getTable("Users") is None:
    database.newTable("Users", "username", "password", "birth", "phone", "country")


async def show():
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
    create_form_label("Under construction!")


@ui.page("/app/join/phone")
def phone():
    header("Create Account")

    form = Form()

    with ui.grid(columns=2):
        create_form_row(
            "Username: ",
            ui.input,
            {"value": username.generate_uname(f"{uuid.uuid4()}", 2)},
        )

        pword = create_form_row(
            "Password: ",
            ui.input,
            {
                "password_toggle_button": True,
                "value": password.generate_password(f"{uuid.uuid4()}", 14),
            },
        )

        pword_cfm = create_form_row(
            "Confirm Password: ",
            ui.input,
            {"password": True, "password_toggle_button": True},
        )

        date = create_form_row(
            "Date of Birth",
            create_date_input,
            {"on_change_callback": lambda e: formValidCheck(e)},
        )

        create_form_row(
            "Phone Number: ", ui.number, {"placeholder": "Without country code"}
        )

        with ui.element("div").classes("p-2 bg-orange-100"):
            create_form_label("Country Code: ")
        with ui.element("div").classes("p-2 bg-blue-100"):
            with ui.row():
                create_form_label("+", color=0x222)
                ui.number(
                    placeholder="91",
                    on_change=lambda e: result.set_text(phones.where(f"+{e.value}")[0]),
                ).props("rounded outlined dense").style("width: 60%;")
                result = ui.label()

    fields = get_form_fields()

    def custom_validation():
        return pword_cfm.value == pword.value

    formValidCheck = setup_validation(
        form, fields, date, {"min_age": env.MIN_AGE}, custom_validation
    )

    def createAccount(e):
        if form.valid:
            if database.hasCell("Users", "username", fields[0].value):
                ui.notify("That username is taken!")
            else:
                database.addRow("Users", *unique([field.value for field in fields]))
                ui.navigate.to("/app/users")

    ui.button("Create Account").props("rounded outlined").bind_enabled_from(
        form, "valid"
    ).on("click", createAccount)
