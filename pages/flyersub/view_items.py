from nicegui import ui
import utils
from utils.addresses import justCountry
import itertools


@utils.logInOnly
def show():
    def showPage(start):
        body.clear()

        with body:
            for _, item in itertools.islice(items.iterrows(), start, start + 5):
                if item["requester"] != uname:
                    with ui.card().classes("box"):
                        ui.label(f"👤 {item['requester']}").style("font-size: 75%")

                        utils.section(item["name"]).classes("justify-center")

                        ui.label(f"From: {justCountry(item['from'])}").classes(
                            "justify-center"
                        )
                        ui.label(f"To: {justCountry(item['to'])}").classes(
                            "justify-center"
                        )

                        ui.label(f"Date: {item['date']}")
                        ui.label(f"Price: SG ${item['price']}")
                        if item["image"]:
                            ui.image(item["image"]).style("max-height: 200px")

                        with ui.row().classes("justify-end"):
                            ui.button(icon="message").props("fab mini").on_click(
                                lambda _, requester=item["requester"]: ui.navigate.to(
                                    f"/msg/{requester}"
                                )
                            )
                            ui.button(icon="check").props("fab mini").on_click(
                                lambda _, item_id=item["id"]: ui.notify(
                                    f"Offer to deliver item {item_id}"
                                )
                            )

    uname = utils.database.getTable("Users").iloc[utils.app.storage.user["logIn"]][  # type: ignore
        "username"
    ]

    items = utils.database.getTable("Items")

    if items is not None and not items.empty:
        ui.pagination(1, len(items.index), direction_links=True).on_value_change(
            lambda e: showPage(e.value - 1)
        )
        body = ui.element("div")
        showPage(0)

    else:
        ui.label("Nobody's ordered anything yet!").style("font-size: 150%")
        ui.label("Why not be the first?").style("font-size: 150%")
        ui.button("Order Now!").on_click(
            lambda _: ui.navigate.to("/app/request")
        ).classes("bg-secondary")
