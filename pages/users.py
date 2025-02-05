from nicegui import ui, app
from utils import database, section, logout, phones, styles
from .join import formlabel

def show():

    if database.getTable('Users') is None:
        ui.label('Kairy App is closed for maintenance. Please check back later!')

    elif 'logIn' not in app.storage.user:
        # Create a log-in page and use database to check if entered credentials are correct
        # If so, redirect to the user's page
        # If not, display an error message
        with ui.grid(columns=2):
            with ui.element('div').classes('p-2 bg-orange-100'):
                formlabel('Username: ')
            with ui.element('div').classes('p-2 bg-blue-100'):
                uname = ui.input(placeholder='Enter your username').props('rounded outlined dense')

            with ui.element('div').classes('p-2 bg-orange-100'):
                formlabel('Password: ')
            with ui.element('div').classes('p-2 bg-blue-100'):
                pword = ui.input(password=True, password_toggle_button=True, placeholder='Enter your password').props('rounded outlined dense')

        def login(_):
            i, record = database.getRow('Users', 'username', uname.value)

            if not record.empty and record['password'][0] == pword.value:
                app.storage.user['logIn'] = i.to_list()[0]
                ui.navigate.to('/')
            else:
                ui.notify('Incorrect username or password', color='red')

        ui.button('Log In').on_click(login)

    else:
        i = app.storage.user['logIn']
        record = database.getTable('Users').iloc[i]
        section(f'Welcome back, {record['username']}!')

        with ui.card().classes('info'):
            ui.label(f'Date-of-birth: {record['birth']}').classes('text-h5')
            ui.label(f'Phone number: +{record['country']:.0f} {record['phone']:,.0f}'.replace(',', ' ')).classes('text-h5')
            ui.label(f'Country: {' '.join(phones.where(record['country']))}').classes('text-h5')
            
            with ui.row():
                ui.button('Edit Profile')
                ui.button('Log Out').on_click(logout).props(f'color=red')