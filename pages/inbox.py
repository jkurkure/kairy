import functools
import nicegui
import utils


@utils.logInOnly
def show():
    utils.header("Inbox")
    utils.styles("main")

    user = utils.users().iloc[nicegui.app.storage.user["logIn"]]["username"]
    messages = nicegui.app.storage.general.get("messages", {})

    convs = utils.unique([conv for conv in messages])

    for conv in convs:
        if user in conv:
            if conv.startswith(user):
                other_user = conv.replace(user, "").replace("with", "")
            else:
                other_user = conv.replace("with", "").replace(user, "")
            with nicegui.ui.card().classes("box"):
                nicegui.ui.label(f"Conversation with {other_user}")
                nicegui.ui.button(icon="open_in_new").props("outline round").on_click(
                    functools.partial(nicegui.ui.navigate.to, f"/msg/{other_user}")
                )
