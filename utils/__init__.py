from nicegui import ui
import re
import pandas as pd

# Here are some helper functions and variables
def header(title):
    ui.page_title('Kairy')
    with ui.header():
        with ui.row().classes('text-h4'):
            ui.label('🏠').on('click', js_handler='''() => {
            window.location.href = '/';
            }''').style('cursor: pointer;')

            ui.label(f'| {title}')

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