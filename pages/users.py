from nicegui import ui, app
from utils import database, section, logout, phones, randCC, randFullName, fieldType
from .join import formlabel
import base64
from random import randrange
import time

if "profile-pics" not in app.storage.general:
    app.storage.general["profile-pics"] = {}

if database.getTable("Payment Methods") is None:
    database.newTable(
        "Payment Methods",
        "username",
        "Card Number",
        "Card Holder Name",
        "Security Code",
        "Expiry Month",
        "Expiry Year",
    )

def setProfilePic(e):
    ui.notify(f"Uploaded {e.name}")
    rawData = base64.b64encode(e.content.read())

    uname = (database.getTable("Users").iloc[app.storage.user["logIn"]])["username"]  # type: ignore
    app.storage.general["profile-pics"][
        uname
    ] = f"data:{e.type};base64,{rawData.decode()}"
    ui.navigate.to("/app/users")

def show():
    if database.getTable("Users") is None:
        ui.label("Kairy App is closed for maintenance. Please check back later!")

    elif "logIn" not in app.storage.user:
        # Create a log-in page and use database to check if entered credentials are correct
        # If so, redirect to the user's page
        # If not, display an error message
        with ui.grid(columns=2):
            with ui.element("div").classes("p-2 bg-orange-100"):
                formlabel("Username: ")
            with ui.element("div").classes("p-2 bg-blue-100"):
                uname = ui.input(placeholder="Enter your username").props(
                    "rounded outlined dense"
                )

            with ui.element("div").classes("p-2 bg-orange-100"):
                formlabel("Password: ")
            with ui.element("div").classes("p-2 bg-blue-100"):
                pword = ui.input(
                    password=True,
                    password_toggle_button=True,
                    placeholder="Enter your password",
                ).props("rounded outlined dense")

        def login(_):
            i, record = database.getRow("Users", "username", uname.value)

            if not record.empty and record["password"][0] == pword.value:
                app.storage.user["logIn"] = i.to_list()[0]
                ui.navigate.to("/")
            else:
                ui.notify("Incorrect username or password", color="red")
        ui.button("Log In").on_click(login)

    else:
        i = app.storage.user["logIn"]
        record = database.getTable("Users").iloc[i]  # type: ignore
        section(f"Welcome back, {record['username']}!")

        with ui.card().classes("box"):
            pp_off = record["username"] not in app.storage.general["profile-pics"]
            with ui.grid(columns=1 if pp_off else 2):
                if not pp_off:
                    ui.image(
                        app.storage.general["profile-pics"][record["username"]]
                    ).style("max-height: 280px")

                with ui.column():
                    section(f"{'Add' if pp_off else 'Change'} Profile Picture")
                    ui.upload(
                        on_upload=setProfilePic,
                        on_rejected=lambda: ui.notify(
                            "Profile Picture is maximum 4.5MB!"
                        ),
                        max_file_size=4_500_000,
                        max_files=1,
                    ).classes("max-w-full")

        with ui.card().classes("info"):
            ui.label(f"Date-of-birth: {record['birth']}").classes("text-h5")
            ui.label(
                f"Phone number: +{record['country']:.0f} {record['phone']:,.0f}".replace(
                    ",", " "
                )
            ).classes("text-h5")
            ui.label(f"Country: {' '.join(phones.where(record['country']))}").classes(
                "text-h5"
            )

            with ui.row():
                ui.button("Edit Profile")
                ui.button("Log Out").on_click(logout).props(f"color=red")

        with ui.card().classes(
            "box"
            if (
                cc_off := not database.hasCell(
                    "Payment Methods", "username", record["username"]
                )
            )
            else "info"
        ):
            with ui.grid(columns=1 if cc_off else 2):
                if not cc_off:
                    with ui.column().classes("items-center"):
                        cc_record = database.getRow(
                            "Payment Methods", "username", record["username"]
                        )[1]

                        for cc_field in database.getTable("Payment Methods").columns:  # type: ignore
                            if cc_field != "username":
                                ui.label(
                                    f"{cc_field}: {cc_record[cc_field][0]}"
                                ).classes("text-h5")

                with ui.column().classes("items-center"):
                    section(f"{'Add' if cc_off else 'Change'} Payment Method")
                    with ui.dialog() as pay_dialog, ui.card().classes("items-center"):
                        section("Enter your payment details")

                        with ui.grid(columns=2):
                            with ui.element("div").classes("p-2 bg-orange-100"):
                                formlabel("Card Number: ")
                            with ui.element("div").classes("p-2 bg-blue-100"):
                                ui.number(placeholder=randCC()).props(
                                    "rounded outlined dense"
                                )

                            with ui.element("div").classes("p-2 bg-orange-100"):
                                formlabel("Card Holder Name: ")
                            with ui.element("div").classes("p-2 bg-blue-100"):
                                ui.input(placeholder=randFullName()).props(
                                    "rounded outlined dense"
                                )

                            with ui.element("div").classes("p-2 bg-orange-100"):
                                formlabel("Security Code: ")
                            with ui.element("div").classes("p-2 bg-blue-100"):
                                ui.number(placeholder=randrange(100, 999)).props("rounded outlined dense")  # type: ignore

                            with ui.element("div").classes("p-2 bg-orange-100"):
                                formlabel("Expiry Date: ")
                            with ui.element("div").classes("p-2 bg-blue-100"):
                                with ui.row().classes("no-wrap"):
                                    ui.number(placeholder="MM").props(
                                        "rounded outlined dense"
                                    )
                                    ui.label("/")
                                    ui.number(placeholder="YYYY").props(
                                        "rounded outlined dense"
                                    )

                        def pay_submit(e):
                            database.addRow(
                                "Payment Methods",
                                record["username"],
                                *[
                                    x.value
                                    for x in pay_dialog.descendants()
                                    if isinstance(x, fieldType)
                                ],
                            )
                            pay_dialog.close()
                            ui.notify("Payment method added successfully!")
                            time.sleep(0.5)
                            ui.navigate.to("/app/users")
                        with ui.row():
                            ui.button(icon="check", on_click=pay_submit).props(
                                "fab color=green"
                            )
                            ui.button(icon="close", on_click=pay_dialog.close).props(
                                "fab color=red"
                            )

                    ui.button(icon="wallet", on_click=pay_dialog.open).props(
                        "fab color=accent"
                    )

                    if not cc_off:

                        def remove_cc(_):
                            database.delRow(
                                "Payment Methods", "username", record["username"]
                            )
                            ui.navigate.to("/app/users")
                        section("Remove Payment Method")
                        ui.button(icon="delete", on_click=remove_cc).props(
                            "fab color=orange"
                        )
