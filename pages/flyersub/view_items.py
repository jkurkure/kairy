from nicegui import ui
import utils
from utils.addresses import justCountry

def show():
    items = utils.database.getTable("Items")
    if items is not None and not items.empty:
        for _, item in items.iterrows():
            with ui.card().classes("box"):
                utils.section(item['name']).classes("justify-center")

                ui.label(f"From: {justCountry(item['from'])}").classes("justify-center")
                ui.label(f"To: {justCountry(item['to'])}").classes("justify-center")

                
                ui.label(f"Date: {item['date']}")
                ui.label(f"Price: {item['price']}")
                if item['image']:
                    ui.image(item['image']).style("max-height: 200px")
    else:
        ui.label("Nobody's ordered anything yet!").style("font-size: 150%")
        ui.label("Why not be the first?").style("font-size: 150%")
        ui.button("Order Now!").on_click(lambda _: ui.navigate.to("/app/request")).classes("bg-secondary")