from functools import partial
from nicegui import ui, app

from utils import header, logInOnly
from utils.database import getTable
from utils.dialogs import severe_error_dialog


def messages(user, other):
    if user >= other:
        conv = f"{other}with{user}"
    else:
        conv = f"{user}with{other}"

    if "messages" not in app.storage.general:
        app.storage.general["messages"] = {conv: []}
    elif conv not in app.storage.general["messages"]:
        app.storage.general["messages"][conv] = []

    return app.storage.general["messages"][conv]


@ui.refreshable
def chat_messages(own_id, other):
    for user_id, avatar, text in messages(own_id, other):
        ui.chat_message(avatar=avatar, text=text, sent=user_id == own_id)


@ui.page("/msg/{other}")
@logInOnly
def index(other: str):
    header(f"Messaging {other}")

    if not (users := getTable("Users")):
        severe_error_dialog().open()
        user = None
    else:
        user = users.iloc[app.storage.user["logIn"]]["username"]

    def send(other):
        messages(user, other).append((user, avatar, text.value))
        chat_messages.refresh()
        text.value = ""

    if (
        "profile-pics" in app.storage.general
        and user in app.storage.general["profile-pics"]
    ):
        avatar = app.storage.general["profile-pics"][user]
    else:
        avatar = f"https://robohash.org/{user}?bgset=bg2"

    with ui.column().classes("w-full items-stretch"):
        chat_messages(user, other)

    with ui.footer().classes("bg-white"):
        with ui.row().classes("w-full items-center"):
            with ui.avatar():
                ui.image(avatar)
            text = (
                ui.input(placeholder="message")
                .props("rounded outlined")
                .classes("flex-grow")
                .on("keydown.enter", partial(send, other))
            )
