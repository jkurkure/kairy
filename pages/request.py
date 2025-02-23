import base64
import datetime
import uuid
import nicegui
import nicegui.events as events
import utils
import utils.addresses as addresses
import utils.phones as phones
import pages.join as join
import env


address_autocomplete = []

if utils.database.getTable("Items") is None:
    utils.database.newTable(
        "Items", "id", "requester", "name", "from", "to", "date", "price", "image"
    )


def location(record, formValidCheck):
    with nicegui.ui.input("Location", autocomplete=address_autocomplete) as location:
        with location.add_slot("append"):
            with nicegui.ui.menu().props("no-parent-event") as menu:
                utils.section("Find your drop-off point")

                def findPlace(e):
                    lat, lng = addresses.lookFor(e.sender.value)
                    if lat and lng:
                        m.center = (lat, lng)
                        m.zoom = 14

                with nicegui.ui.row():
                    with nicegui.ui.input().on("blur", findPlace) as search:
                        search.classes("no-form")
                        with search.add_slot("prepend"):
                            search_icon = nicegui.ui.icon("search").classes("cursor-pointer")

                m = nicegui.ui.leaflet(
                    center=addresses.getCenter(phones.where(record["country"])), zoom=10
                )  # type: ignore

                test_mark = m.marker(latlng=(1.3521, 103.8198))

                def handle_click(e: events.GenericEventArguments):
                    for layer in m.layers:
                        if isinstance(layer, type(test_mark)):
                            m.remove_layer(layer)

                    lat = e.args["latlng"]["lat"]
                    lng = e.args["latlng"]["lng"]
                    m.marker(latlng=(lat, lng))
                    m.center = (lat, lng)
                    m.zoom = 19

                    location.value = addresses.getName(lat, lng)
                    address_autocomplete.append(location.value)
                    formValidCheck(e)

                m.on("map-click", handle_click)

                with nicegui.ui.row().classes("justify-end"):
                    nicegui.ui.button("Close", on_click=menu.close).props("flat")

            nicegui.ui.icon("pin_drop").on("click", menu.open).classes("cursor-pointer")


def show():
    photo = ""

    if "logIn" not in nicegui.app.storage.user:
        nicegui.ui.navigate.to("/app/join")

    else:
        i = nicegui.app.storage.user["logIn"]
        record = utils.database.getTable("Users").iloc[i]  # type: ignore

        setattr(form := utils.Form(), "valid", False)

        utils.section("Tell us more!")

        with nicegui.ui.grid(columns=2):
            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("Item name: ")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                nicegui.ui.input(
                    validation=lambda value: (
                        "Only letters in your item's name please"
                        if not value.replace(" ", "").isalpha()
                        else None
                    )
                ).props("rounded outlined dense")

            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("Where can it be picked up?")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                location(record, lambda e: formValidCheck(e))

            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("Where do you want it delivered?")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                location(record, lambda e: formValidCheck(e))

            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("When do you want it delivered?")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                with nicegui.ui.input("Date") as date:
                    with nicegui.ui.menu().props("no-parent-event") as menu:
                        with nicegui.ui.date().bind_value(date).on_value_change(
                            lambda e: formValidCheck(e)
                        ):
                            with nicegui.ui.row().classes("justify-end"):
                                nicegui.ui.button("Close", on_click=menu.close).props("flat")
                    with date.add_slot("append"):
                        nicegui.ui.icon("edit_calendar").on("click", menu.open).classes(
                            "cursor-pointer"
                        )

            with nicegui.ui.element("div").classes("p-2 bg-orange-100"):
                join.formlabel("How much are you offering?")
            with nicegui.ui.element("div").classes("p-2 bg-blue-100"):
                nicegui.ui.number(min=2.50, max=100, step=0.01, prefix="SG $")

        fields = [f for f in list(nicegui.ElementFilter(kind=utils.fieldType)) if "no-form" not in f.classes]  # type: ignore

        def formValidCheck(_):
            form.valid = (False not in [field.value not in [None, ""] and not (field.validation and field.validation(field.value)) for field in fields]) and utils.dateCheck(date.value, allow_yrs=range(datetime.datetime.now().year, datetime.datetime.now().year + env.MAX_ADVANCE_YRS + 1))  # type: ignore

        [field.on("change", formValidCheck) for field in fields]

        utils.section("Attach a photo")

        def setPhoto(e):
            nonlocal photo
            nicegui.ui.notify(f"Uploaded {e.name}")
            rawData = base64.b64encode(e.content.read())

            photo = f"data:{e.type};base64,{rawData.decode()}"

        nicegui.ui.upload(
            on_upload=setPhoto,
            on_rejected=lambda: nicegui.ui.notify("Profile Picture is maximum 4.5MB!"),
            max_file_size=4_500_000,
            max_files=1,
        ).classes("max-w-full")

        def listItem(e):
            if form.valid:  # type: ignore
                utils.database.addRow(
                    "Items",
                    *utils.unique(
                        [uuid.uuid4(), record["username"]]
                        + [field.value for field in fields]
                        + [photo]
                    ),
                )
                nicegui.ui.navigate.to("/app/users")

        nicegui.ui.button("List").props("rounded outlined").bind_enabled_from(form, "valid").on(
            "click", listItem
        )
