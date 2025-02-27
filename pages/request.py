import base64
import functools
import uuid
import nicegui
from utils import database, logInOnly, unique
import env
import utils.dialogs as dialogs
from utils.forms import (
    Form,
    create_form_label,
    create_date_input,
    create_location_input,
    get_form_fields,
    setup_validation,
    create_form_row,
)

address_autocomplete = []

if database.getTable("Items") is None:
    database.newTable(
        "Items", "id", "requester", "name", "from", "to", "date", "price", "image"
    )


@logInOnly
def show():
    photo = ""

    i = nicegui.app.storage.user["logIn"]
    record = database.getTable("Users").iloc[i]  # type: ignore

    form = Form()

    create_form_label("Tell us more!")

    with nicegui.ui.grid(columns=2):
        create_form_row(
            "Item name: ",
            nicegui.ui.input,
            {
                "validation": lambda value: (
                    "Only letters in your item's name please"
                    if not value.replace(" ", "").isalpha()
                    else None
                )
            },
        )

        fvcWrap = lambda e: formValidCheck(e)

        # Create location inputs
        def loc_kwargs(point_type):
            return {
                "record": record,
                "address_autocomplete": address_autocomplete,
                "formValidCheck": fvcWrap,
                "inner_prompt": f"Find your {point_type} point",
            }

        create_form_row(
            "Where can it be picked up?",
            create_location_input,
            loc_kwargs("pick-up"),
        )

        create_form_row(
            "Where do you want it delivered?",
            create_location_input,
            loc_kwargs("drop-off"),
        )

        date = create_form_row(
            "When do you want it delivered?",
            create_date_input,
            {"on_change_callback": fvcWrap},
        )

        create_form_row(
            "How much are you offering?",
            nicegui.ui.number,
            {"min": 2.50, "max": 100, "step": 0.01, "prefix": "SG $"},
        )

    fields = get_form_fields(exclude_classes=["no-form"])

    # Now define formValidCheck
    formValidCheck = setup_validation(
        form, fields, date, {"max_advance_yrs": env.MAX_ADVANCE_YRS}
    )

    create_form_label("Attach a photo")

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
        if form.valid:
            database.addRow(
                "Items",
                *unique(
                    [uuid.uuid4(), record["username"]]
                    + [field.value for field in fields]
                    + [photo]
                ),
            )
            success_dialog = dialogs.order_success_dialog(
                functools.partial(nicegui.ui.navigate.to, "/app/users")
            )
            success_dialog.open()

    nicegui.ui.button("List").props("rounded outlined").bind_enabled_from(
        form, "valid"
    ).on("click", listItem)
