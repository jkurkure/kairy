from nicegui import ui
from utils import section
import env

def show():
    section(f"{env.APP_NAME} hopes to bring deliveries to the people!")
    section(f"Brought to you by {env.authors()}")
    ui.label(f"You are currently using version {env.APP_VERSION}")

