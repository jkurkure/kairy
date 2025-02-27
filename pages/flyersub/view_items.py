from functools import partial
from nicegui import ui
import utils
from utils.addresses import justCountry

ITEMS_PER_PAGE = 5


@utils.logInOnly
def show():
    uname = utils.database.getTable("Users").iloc[utils.app.storage.user["logIn"]][
        "username"
    ]

    with ui.element("div") as container:

        items = utils.database.getTable("Items")
        if items is not None and not items.empty:
            total_items = len(items)
            total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

            def display_page(page):
                container.clear()
                start = (page - 1) * ITEMS_PER_PAGE
                end = start + ITEMS_PER_PAGE

                with ui.row().classes("justify-center"):
                    for p in range(1, total_pages):
                        ui.button(f"Page {p}").props("fab mini").on_click(
                            lambda _, p=p: display_page(p)
                        )

                for _, item in items.iloc[start:end].iterrows():
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
                                    lambda _, requester=item[
                                        "requester"
                                    ]: ui.navigate.to(f"/msg/{requester}")
                                )
                                ui.button(icon="check").props("fab mini").on_click(
                                    lambda _, item_id=item["id"]: ui.notify(
                                        f"Offer to deliver item {item_id}"
                                    )
                                )

            display_page(1)
        else:
            ui.label("Nobody's ordered anything yet!").style("font-size: 150%")
            ui.label("Why not be the first?").style("font-size: 150%")
            ui.button("Order Now!").on_click(
                lambda _: ui.navigate.to("/app/request")
            ).classes("bg-secondary")
