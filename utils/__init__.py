from nicegui import ui, app
import re, rstr, random
import pandas as pd
from .database import getTable
from names_dataset import NameDataset

nd = NameDataset()
lastNames = list(nd.get_top_names(n=100, use_first_names=False, country_alpha2='SG')['SG'])
firstNames = list(nd.get_top_names(n=100, country_alpha2='SG')['SG']['M']) + list(nd.get_top_names(n=100, country_alpha2='SG')['SG']['F'])

# Here are some helper functions and variables
def logout():
    app.storage.user.clear()
    ui.navigate.to('/app/users')

def header(title):
    ui.page_title('Kairy')
    with ui.header().classes('justify-between'):
        with ui.row().classes('text-h4'):
            ui.label('🏠').on('click', js_handler='''() => {
            window.location.href = '/';
            }''').style('cursor: pointer;')

            ui.label(f'| {title}')

        if 'logIn' in app.storage.user:
            with ui.grid(columns=2):
                uname = getTable('Users').iloc[app.storage.user['logIn']]['username'] # type: ignore
                ui.image(app.storage.general['profile-pics'][uname]).style('max-width: 90px')
                with ui.column().classes('items-center'):
                    ui.label(f'👤 {uname}')
                    ui.button('Log Out', on_click=logout).classes('bg-secondary')

def find(L, v, i):
    for x in L:
        if x[0] == v:
            return x[i]

def styles(path):
    with open(f'styles/{path}.css') as f:
        # This is how we add custom CSS (or any other header HTML) to the webpage
        ui.add_head_html(f'''
            <style type="text/tailwindcss">
                {f.read()}
            </style>
        ''')

def section(text, color=0x6E93D6, size=200):
    ui.label(text).style(f'color: #{color:x}; font-size: {size}%; font-weight: 300')

class Form:
    pass

def dateCheck(date):
    return re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.IGNORECASE).match(date)

def unique(L):
    return pd.Series(L).unique().tolist()

def randCC():
    return f'{int(rstr.xeger(r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$')):,}'.replace(',', ' ')

def randFullName():
    return f'{random.choice(firstNames)} {random.choice(lastNames)}'