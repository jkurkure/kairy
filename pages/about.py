from nicegui import ui
from utils import section
import env
from utils import codename as cn


def show():
    section(f"{env.APP_NAME} hopes to bring deliveries to the people!")
    section(f"Brought to you by {env.authors()}")
    ui.label(f"You are currently using version {cn.get(env.APP_VERSION)} ({env.APP_VERSION})")
