import nicegui
import utils
import utils.phones as phones
import pages.join as join
import base64
import random
import time
import datetime
import env

if "profile-pics" not in nicegui.app.storage.general:
    nicegui.app.storage.general["profile-pics"] = {}

if utils.database.getTable("Payment Methods") is None:
    utils.database.newTable(
        "Payment Methods",
        "username",
        "Card Number",
        "Card Holder Name",
        "Security Code",
        "Expiry Month",
        "Expiry Year",
    )


def setProfilePic(e):
    nicegui.ui.notify(f"Uploaded {e.name}")
    rawData = base64.b64encode(e.content.read())

    uname = (utils.database.getTable("Users").iloc[nicegui.app.storage.user["logIn"]])["username"]  # type: ignore
    nicegui.app.storage.general["profile-pics"][
        uname
    ] = f"data:{e.type};base64,{rawData.decode()}"
    nicegui.ui.navigate.to("/app/users")


def show():
    if utils.database.getTable("Users") is None:
        env.maintenance()

    elif "logIn" not in nicegui.app.storage.user:
        # Create a log-in page and use database to check if entered credentials are correct
        # If so, redirect to the user's page
        # If not, display an error message
        with nicegui.ui.grid(columns=2):
            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("Username: ")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                uname = nicegui.ui.input(placeholder="Enter your username").props(
                    "rounded outlined dense"
                )

            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("Password: ")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                pword = nicegui.ui.input(
                    password=True,
                    password_toggle_button=True,
                    placeholder="Enter your password",
                ).props("rounded outlined dense")

        def login(_):
            i, record = utils.database.getRow("Users", "username", uname.value)
            if (
                not record.empty
                and record["password"][ID := i.to_list()[0]] == pword.value
            ):
                nicegui.app.storage.user["logIn"] = ID
                nicegui.ui.navigate.to("/")
            else:
                nicegui.ui.notify("Incorrect username or password", color="red")

        nicegui.ui.button("Log In").on_click(login)

    else:
        i = nicegui.app.storage.user["logIn"]
        record = utils.database.getTable("Users").iloc[i]  # type: ignore
        utils.section(f"Welcome back, {record['username']}!")

        with nicegui.ui.card().classes("box"):
            pp_off = (
                record["username"] not in nicegui.app.storage.general["profile-pics"]
            )
            with nicegui.ui.grid(columns=1 if pp_off else 2):
                if not pp_off:
                    nicegui.ui.image(
                        nicegui.app.storage.general["profile-pics"][record["username"]]
                    ).style("max-height: 280px")

                with nicegui.ui.column():
                    utils.section(f"{'Add' if pp_off else 'Change'} Profile Picture")
                    nicegui.ui.upload(
                        on_upload=setProfilePic,
                        on_rejected=lambda: nicegui.ui.notify(
                            "Profile Picture is maximum 4.5MB!"
                        ),
                        max_file_size=4_500_000,
                        max_files=1,
                    ).classes("max-w-full")

        with nicegui.ui.card().classes("info"):
            nicegui.ui.label(f"Date-of-birth: {record['birth']}").classes("text-h5")
            nicegui.ui.label(
                f"Phone number: +{record['country']:.0f} {record['phone']:,.0f}".replace(
                    ",", " "
                )
            ).classes("text-h5")
            nicegui.ui.label(
                f"Country: {' '.join(phones.where(record['country']))}"
            ).classes("text-h5")

            with nicegui.ui.row():
                nicegui.ui.button("Edit Profile")
                nicegui.ui.button("Log Out").on_click(utils.logout).props(f"color=red")

        with nicegui.ui.card().classes(
            "box"
            if (
                cc_off := not utils.database.hasCell(
                    "Payment Methods", "username", record["username"]
                )
            )
            else "info"
        ):
            with nicegui.ui.grid(columns=1 if cc_off else 2):
                if not cc_off:
                    with nicegui.ui.column().classes("items-center"):
                        cc_record = utils.database.getRow(
                            "Payment Methods", "username", record["username"]
                        )[1]

                        for cc_field in utils.database.getTable("Payment Methods").columns:  # type: ignore
                            if cc_field != "username":
                                nicegui.ui.label(
                                    f"{cc_field}: {cc_record[cc_field][0]}"
                                ).classes("text-h5")

                with nicegui.ui.column().classes("items-center"):
                    utils.section(f"{'Add' if cc_off else 'Change'} Payment Method")
                    with nicegui.ui.dialog() as pay_dialog, nicegui.ui.card().classes(
                        "items-center"
                    ):
                        utils.section("Enter your payment details")

                        with nicegui.ui.grid(columns=2):
                            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                                join.formlabel("Card Number: ")
                            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                                nicegui.ui.number(
                                    placeholder=utils.randCC(), min=1e15, max=1e20
                                ).props("rounded outlined dense")

                            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                                join.formlabel("Card Holder Name: ")
                            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                                nicegui.ui.input(
                                    placeholder=utils.randFullName(),
                                    validation=lambda value: (
                                        "Only letters in your name please"
                                        if not value.replace(" ", "").isalpha()
                                        else None
                                    ),
                                ).props("rounded outlined dense")

                            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                                join.formlabel("Security Code: ")
                            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                                nicegui.ui.number(placeholder=random.randrange(100, 999), min=100, max=999).props("rounded outlined dense")  # type: ignore

                            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                                join.formlabel("Expiry Date: ")
                            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                                with nicegui.ui.row().classes("no-wrap"):
                                    nicegui.ui.number(
                                        placeholder="MM", min=1, max=12
                                    ).props("rounded outlined dense")
                                    nicegui.ui.label("/")
                                    nicegui.ui.number(
                                        placeholder="YYYY",
                                        min=datetime.datetime.now().year,
                                    ).props("rounded outlined dense")

                        def pay_submit(e):
                            utils.database.addRow(
                                "Payment Methods",
                                record["username"],
                                *[
                                    x.value
                                    for x in pay_dialog.descendants()
                                    if isinstance(x, utils.fieldType)
                                ],
                            )
                            pay_dialog.close()
                            nicegui.ui.notify("Payment method added successfully!")
                            time.sleep(0.5)
                            nicegui.ui.navigate.to("/app/users")

                        with nicegui.ui.row():
                            nicegui.ui.button(icon="check", on_click=pay_submit).props(
                                "fab color=green"
                            )
                            nicegui.ui.button(
                                icon="close", on_click=pay_dialog.close
                            ).props("fab color=red")

                    nicegui.ui.button(icon="wallet", on_click=pay_dialog.open).props(
                        "fab color=accent"
                    )

                    if not cc_off:

                        def remove_cc(_):
                            utils.database.delRow(
                                "Payment Methods", "username", record["username"]
                            )
                            nicegui.ui.navigate.to("/app/users")

                        utils.section("Remove Payment Method")
                        nicegui.ui.button(icon="delete", on_click=remove_cc).props(
                            "fab color=orange"
                        )
