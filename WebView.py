from nicegui import ui

def open_window():
    # JavaScript to open a new window and remove the address bar
    js_code = """
    var newWindow = window.open('https://us-west.on-air.io/bringka/device-0/', '_blank', 'width=800,height=600');
    newWindow.onload = function() {
        newWindow.document.documentElement.style.overflow = 'hidden';  // Hide scrollbars
        newWindow.document.body.style.margin = '0';  // Remove margin
        newWindow.document.body.style.padding = '0';  // Remove padding
        newWindow.document.body.style.height = '100%';  // Full height
        newWindow.document.body.style.width = '100%';  // Full width
        newWindow.document.body.style.position = 'fixed';  // Prevent scrolling
    };
    """
    ui.run_javascript(js_code)

with ui.grid(columns=2):
    ui.button('Open Bringka in Your Browser', on_click=open_window)
    ui.button('Download Bringka as Chrome App', on_click=None) # TO-DO

    ui.button('Get Bringka from the Play Store', on_click=None) # TO-DO
    ui.button('Get Bringka from the App Store', on_click=None) # TO-DO

ui.run()