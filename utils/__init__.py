import functools
import pickle
from nicegui import ui, app
import re, rstr, random
import pandas as pd
from .database import getTable
import env
from starlette.formparsers import MultiPartParser


# Here are some helper functions and variables

fieldType = ui.input | ui.number
firstNames, lastNames = pickle.load(open("resources/data/names.pkl", "rb"))
MultiPartParser.max_file_size = 1024 * 1024 * 50

class Form:
    pass


def logout():
    app.storage.user.clear()
    ui.navigate.to("/app/users")


def header(title):
    ui.page_title(env.APP_NAME)
    with ui.header().classes("justify-between no-wrap"):
        with ui.row().classes("text-h4 no-wrap"):
            ui.label("🏠").on("click", lambda _: ui.navigate.to("/")).style(
                "cursor: pointer;"
            )

            ui.label(f"| {title}")

        if "logIn" in app.storage.user:
            uname = getTable("Users").iloc[app.storage.user["logIn"]]["username"]  # type: ignore

            with ui.grid(
                columns=(
                    2 if (pp_set := uname in app.storage.general["profile-pics"]) else 1
                )
            ):
                if pp_set:
                    ui.image(app.storage.general["profile-pics"][uname]).style(
                        "max-width: 90px"
                    )

                with ui.column().classes("items-center"):
                    ui.label(f"👤 {uname}")
                    ui.button("Log Out", on_click=logout).classes("bg-secondary")


def find(L, v, i):
    for x in L:
        if x[0] == v:
            return x[i]


def styles(path):
    with open(f"resources/styles/{path}.css") as f:
        # This is how we add custom CSS (or any other header HTML) to the webpage
        ui.add_head_html(
            f"""
            <style type="text/tailwindcss">
                {f.read()}
            </style>
        """
        )


def section(text, color=0x6E93D6, size=200):
    return ui.label(text).style(
        f"color: #{color:x}; font-size: {size}%; font-weight: 300"
    )


def dateCheck(date, allow_yrs=None):
    return re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.IGNORECASE).match(date) and (
        not (allow_yrs) or int(date[:4]) in allow_yrs
    )


def unique(L):
    return pd.Series(L).unique().tolist()


def randCC():
    ccRegex = r"^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
    return f"{int(rstr.xeger(ccRegex)):,}".replace(",", " ")


def randFullName():
    return f"{random.choice(firstNames)} {random.choice(lastNames)}"


def funcChain(*fs):
    return lambda: [f() for f in fs]


def logInOnly(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "logIn" not in app.storage.user:
            ui.navigate.to("/app/users")
        else:
            return func(*args, **kwargs)

    return wrapper
