from functools import partial
from nicegui import ui, app

from utils import header
from utils.common import easy_hasher
from utils.database import getTable


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
def index(other: str):
    if "logIn" not in app.storage.user:
        ui.navigate.to("/app/users")

    else:
        header(f"Messaging {other}")

        def send(other):
            messages(user, other).append((user, avatar, text.value))
            chat_messages.refresh()
            text.value = ""

        user = getTable("Users").iloc[app.storage.user["logIn"]]["username"]

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
