from nicegui import ui
from functools import partial 
from utils import styles, section, header, username, password, phones
import uuid

registerTypes = [
    ('Phone Number', 'phone'),
    ('Google Accounts', 'google')
]

formlabel = partial(section, size=120)

def show():
    styles('main')

    ui.label("We're so glad you want to join the family!").classes('text-h5')
    
    ui.label('How do you wish to register?')
    
    with ui.row():
        for type, page in registerTypes:
            with ui.card().classes('box').on('click', partial(ui.navigate.to, f'/app/join/{page}')):
                section(type)


# Sub-pages
@ui.page('/app/join/google')
def google():
    header('Create Account')
    section('Under construction!')

@ui.page('/app/join/phone')
def phone():
    header('Create Account')

    with ui.grid(columns=2):
        with ui.element('div').classes('p-2 bg-orange-100'):
            formlabel('Phone Number: ')
        with ui.element('div').classes('p-2 bg-blue-100'):
            ui.number(placeholder='Without country code').props('rounded outlined dense')

        with ui.element('div').classes('p-2 bg-orange-100'):
            formlabel('Country Code: ')
        with ui.element('div').classes('p-2 bg-blue-100'):
            with ui.row():
                formlabel('+', color=0x222)
                ui.number(placeholder='91', on_change=lambda e: result.set_text(phones.where(f'+{e.value}')[0])).props('rounded outlined dense').style('width: 60%;')
                result = ui.label()

        with ui.element('div').classes('p-2 bg-orange-100'):
            formlabel('Username: ')
        with ui.element('div').classes('p-2 bg-blue-100'):
            ui.input(value=username.generate_uname(f'{uuid.uuid4()}', 2)).props('rounded outlined dense')


        with ui.element('div').classes('p-2 bg-orange-100'):
            formlabel('Password: ')
        with ui.element('div').classes('p-2 bg-blue-100'):
            ui.input(password_toggle_button=True, value=password.generate_password(f'{uuid.uuid4()}', 14)).props('rounded outlined dense')


        with ui.element('div').classes('p-2 bg-orange-100'):
            formlabel('Confirm Password: ')
        with ui.element('div').classes('p-2 bg-blue-100'):
            ui.input(password=True, password_toggle_button=True).props('rounded outlined dense')    