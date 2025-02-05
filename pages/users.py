from nicegui import ui
from utils import database

def show():
    if database.getTable('Users') is None:
        ui.label('We could put an interactive list of all users here')

    else:
        database.showTable('Users')