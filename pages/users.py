from nicegui import ui, app
from utils import database, section, logout, phones, styles
from .join import formlabel
import base64

if 'profile-pics' not in app.storage.general:
    app.storage.general['profile-pics'] = {}


def setProfilePic(e):
    ui.notify(f'Uploaded {e.name}')
    rawData = base64.b64encode(e.content.read())

    uname = (database.getTable('Users').iloc[app.storage.user['logIn']])['username']
    app.storage.general['profile-pics'][uname] = f'data:{e.type};base64,{rawData.decode()}'
    ui.navigate.to('/app/users')

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

        with ui.card().classes('box'):
            pp_off = record['username'] not in app.storage.general['profile-pics']
            with ui.grid(columns=1 if pp_off else 2):
                ui.image(app.storage.general['profile-pics'][record['username']]).style('max-width: 180px')
                
                with ui.column():
                    section(f'{'Add' if pp_off else 'Change'} Profile Picture')
                    ui.upload(on_upload=setProfilePic,
                        on_rejected=lambda: ui.notify('Profile Picture is maximum 3.5MB!'),
                        max_file_size=3_500_000, max_files=1).classes('max-w-full')

        with ui.card().classes('info'):
            ui.label(f'Date-of-birth: {record['birth']}').classes('text-h5')
            ui.label(f'Phone number: +{record['country']:.0f} {record['phone']:,.0f}'.replace(',', ' ')).classes('text-h5')
            ui.label(f'Country: {' '.join(phones.where(record['country']))}').classes('text-h5')
            
            with ui.row():
                ui.button('Edit Profile')
                ui.button('Log Out').on_click(logout).props(f'color=red')