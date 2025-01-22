from nicegui import ui

# Here are some helper functions and variables
def header(title):
    ui.page_title('Kairy')
    with ui.header():
        with ui.row().classes('text-h3'):
            ui.label('🏠').on('click', js_handler='''() => {
            window.location.href = '/';
            }''').style('cursor: pointer;')

            ui.label(f'| {title}')

def find(L, v, i):
    for x in L:
        if x[0] == v:
            return x[i]