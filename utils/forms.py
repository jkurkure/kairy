# utils/forms.py - New file to hold common form functionality

from nicegui import ElementFilter, ui
from datetime import datetime
from utils import fieldType, dateCheck, section


null = lambda _: None

class Form:
    def __init__(self):
        self.valid = False

def create_form_label(*args, **kwargs):
    if 'size' not in kwargs:
        kwargs['size'] = 120
    return section(*args, **kwargs)

def create_date_input(on_change_callback=None):
    """Create a date input with calendar picker"""
    with ui.input("Date") as date:
        with ui.menu().props("no-parent-event") as menu:
            date_picker = ui.date().bind_value(date)
            if on_change_callback:
                date_picker.on_value_change(on_change_callback)
            with ui.row().classes("justify-end"):
                ui.button("Close", on_click=menu.close).props("flat")
        with date.add_slot("append"):
            ui.icon("edit_calendar").on("click", menu.open).classes("cursor-pointer")
    return date

def create_location_input(record={}, address_autocomplete=[], formValidCheck=null, inner_prompt=''):
    """Create a location input with map picker"""
    from utils import addresses, phones
    
    with ui.input("Location", autocomplete=address_autocomplete) as location:
        with location.add_slot("append"):
            with ui.menu().props("no-parent-event") as menu:
                create_form_label(inner_prompt)

                def findPlace(e):
                    lat, lng = addresses.lookFor(e.sender.value)
                    if lat and lng:
                        m.center = (lat, lng)
                        m.zoom = 14

                with ui.row():
                    with ui.input().on("blur", findPlace) as search:
                        search.classes("no-form")
                        with search.add_slot("prepend"):
                            ui.icon("search").classes("cursor-pointer")

                m = ui.leaflet(
                    center=addresses.getCenter(phones.where(record["country"])), zoom=10  # type: ignore
                )
                test_mark = m.marker(latlng=(1.3521, 103.8198))

                def handle_click(e):
                    for layer in m.layers:
                        if isinstance(layer, type(test_mark)):
                            m.remove_layer(layer)

                    lat = e.args["latlng"]["lat"]
                    lng = e.args["latlng"]["lng"]
                    m.marker(latlng=(lat, lng))
                    m.center = (lat, lng)
                    m.zoom = 19

                    location.value = addresses.getName(lat, lng)
                    address_autocomplete.append(location.value)
                    formValidCheck(e)

                m.on("map-click", handle_click)

                with ui.row().classes("justify-end"):
                    ui.button("Close", on_click=menu.close).props("flat")

            ui.icon("pin_drop").on("click", menu.open).classes("cursor-pointer")
    return location

def get_form_fields(exclude_classes=None):
    """Get all form fields except those with specified classes"""
    if exclude_classes:
        return [f for f in list(ElementFilter(kind=fieldType)) if all(cls not in f.classes for cls in exclude_classes)]  # type: ignore
    return list(ElementFilter(kind=fieldType))  # type: ignore

def setup_validation(form, fields, date=None, date_options=None, custom_validation=None):
    """Set up form validation with optional date validation"""
    def formValidCheck(_):
        field_validation = False not in [
            field.value not in [None, ""] and 
            not (hasattr(field, 'validation') and field.validation and field.validation(field.value)) 
            for field in fields
        ]
        
        date_validation = True
        if date and date_options:
            current_year = datetime.now().year
            if 'min_age' in date_options:
                date_validation = dateCheck(date.value, allow_yrs=range(current_year - 100, current_year - date_options['min_age']))
            elif 'max_advance_yrs' in date_options:
                date_validation = dateCheck(date.value, allow_yrs=range(current_year, current_year + date_options['max_advance_yrs'] + 1))
        
        custom_valid = True
        if custom_validation:
            custom_valid = custom_validation()
            
        form.valid = field_validation and date_validation and custom_valid

    for field in fields:
        field.on("change", formValidCheck)
    
    return formValidCheck

def create_form_row(label_text, component, kwargs, props='rounded outlined dense'):
    """Create a standardized form row with orange label background and blue input background"""
    with ui.element("div").classes("p-2 bg-orange-100"):
        create_form_label(label_text)
    with ui.element("div").classes("p-2 bg-blue-100"):
        field = component(**kwargs).props(props)

    return field