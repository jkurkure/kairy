from nicegui import ui, app
from utils import database
from .join import formlabel

def show():
    if database.getTable('Users') is None:
        ui.label('Kairy App is closed for maintenance. Please check back later!')

    else:
        print(app.storage.user)
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
                app.storage.user['logIn'] = i
                ui.navigate.to('/app/users')
            else:
                ui.notify('Incorrect username or password', color='red')

        ui.button('Log In').on_click(login)