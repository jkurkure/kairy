from nicegui import ui
import env


def show():
    ui.label(f"{env.APP_NAME} hopes to bring deliveries to the people!")
