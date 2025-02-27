from pathlib import Path
import subprocess, pickle, sys
from nicegui import ui

PYRUNNER = sys.executable
REPO_NAME = "kairy"
APP_NAME = "Bringka"
APP_VERSION = f'{subprocess.Popen("git rev-parse --short HEAD", shell=True, stdout=subprocess.PIPE).communicate()[0]}'[
    2:-3
]

MIN_AGE = 16
MAX_ADVANCE_YRS = 2

ALLOWED_COUNTRIES = ["India", "Singapore"]


def authors():
    AUTHORS = [
        "Srihari Rangan",
        "Deepankur Njondimackal",
        "Arushi Bhatnagar",
    ]
    return ", ".join(AUTHORS[:-1]) + f" and {AUTHORS[-1]}"


def maintenance():
    ui.label(f"{APP_NAME} App is closed for maintenance. Please check back later!")


def secret(name):
    SECRET_PATH = (
        _def if Path(_def := "/home/private/.secrets").exists() else "../.secrets"
    )

    with open(SECRET_PATH, "rb") as f:
        return pickle.load(f)[name]
