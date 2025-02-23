import base64
from datetime import datetime
from functools import partial
import uuid
from nicegui import ElementFilter, ui, app, events
from utils import database, dateCheck, section, fieldType, Form, unique, phones, addresses
from .join import formlabel
import env


address_autocomplete = []

if database.getTable('Items') is None:
    database.newTable('Items', 'id', 'requester', 'name', 'from', 'to', 'date', 'price', 'image')

def location(record, formValidCheck):
    with ui.input("Location", autocomplete=address_autocomplete) as location:
                    with location.add_slot("append"):
                        with ui.menu().props("no-parent-event") as menu:
                            section('Find your drop-off point')


                            def findPlace(e):
                                lat, lng = addresses.lookFor(e.sender.value)
                                if lat and lng:
                                    m.center = (lat, lng)
                                    m.zoom = 14

                            with ui.row():
                                with ui.input().on('blur', findPlace) as search:
                                    search.classes('no-form')
                                    with search.add_slot("prepend"):
                                        search_icon = ui.icon('search').classes('cursor-pointer')
                                

                            m = ui.leaflet(center=addresses.getCenter(
                                phones.where(record['country'])
                            ), zoom=10) # type: ignore
        

                            test_mark = m.marker(latlng=(1.3521, 103.8198))
                            def handle_click(e: events.GenericEventArguments):
                                for layer in m.layers:
                                    if isinstance(layer, type(test_mark)):
                                        m.remove_layer(layer)
                                
                                lat = e.args['latlng']['lat']
                                lng = e.args['latlng']['lng']
                                m.marker(latlng=(lat, lng))
                                m.center = (lat, lng)
                                m.zoom = 19

                                location.value = addresses.getName(lat, lng)
                                address_autocomplete.append(location.value)
                                formValidCheck(e)
                            m.on('map-click', handle_click)


                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu.close).props("flat")


                        ui.icon("pin_drop").on("click", menu.open).classes(
                            "cursor-pointer"
                        )

def show():
    photo = "" 
    
    if 'logIn' not in app.storage.user:
        ui.navigate.to('/app/join')

    else:
        i = app.storage.user['logIn']
        record = database.getTable('Users').iloc[i] # type: ignore

        setattr(form := Form(), "valid", False)

        section('Tell us more!')

        with ui.grid(columns=2):
            with ui.element("div").classes("p-2 bg-orange-100"):
                formlabel("Item name: ")
            with ui.element("div").classes("p-2 bg-blue-100"):
                ui.input(validation=lambda value: "Only letters in your item's name please" if not value.replace(' ', '').isalpha() else None).props(
                    "rounded outlined dense"
                )


            with ui.element("div").classes("p-2 bg-orange-100"):
                formlabel("Where can it be picked up?")
            with ui.element("div").classes("p-2 bg-blue-100"):
                location(record, lambda e: formValidCheck(e))

            with ui.element("div").classes("p-2 bg-orange-100"):
                formlabel("Where do you want it delivered?")
            with ui.element("div").classes("p-2 bg-blue-100"):
                location(record, lambda e: formValidCheck(e))


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
                ui.number(min = 2.50, max = 100, step = 0.01, prefix="SG $")

        fields = [f for f in list(ElementFilter(kind=fieldType)) if 'no-form' not in f.classes]  # type: ignore

        def formValidCheck(_):
            form.valid = (False not in [field.value not in [None, ""] and not (field.validation and field.validation(field.value)) for field in fields]) and dateCheck(date.value, allow_yrs = range(datetime.now().year, datetime.now().year + env.MAX_ADVANCE_YRS + 1))  # type: ignore 
            

        [field.on("change", formValidCheck) for field in fields]


        section("Attach a photo")

        def setPhoto(e):
            nonlocal photo
            ui.notify(f"Uploaded {e.name}")
            rawData = base64.b64encode(e.content.read())

            photo = f"data:{e.type};base64,{rawData.decode()}"

        ui.upload(
            on_upload=setPhoto,
            on_rejected=lambda: ui.notify(
                "Profile Picture is maximum 4.5MB!"
            ),
            max_file_size=4_500_000,
            max_files=1,
        ).classes("max-w-full")


        def listItem(e):
            if form.valid:  # type: ignore
                database.addRow("Items", *unique([uuid.uuid4(), record['username']] + [field.value for field in fields] + [photo]))
                ui.navigate.to("/app/users")

        ui.button("List").props("rounded outlined").bind_enabled_from(
            form, "valid"
        ).on("click", listItem)
