from nicegui import ui
import importlib

from utils import section
import utils
import sys

# Import the shared navigation functions from App.py
sys.path.append(".")  # Ensure we can import from the root directory
from App import create_navigation_buttons, load_subpage

# Define the flyer subpages
flyer_pages = [
    ("view_items", "list", "View Items"),
    ("add_flight", "flight", "Add Upcoming Flight"),
]


def show():
    # Use the shared navigation function with a custom base path
    create_navigation_buttons(flyer_pages, base_path="/app/flyer")


@ui.page("/app/flyer/{subpage}")
def App(subpage: str):
    # Use the shared subpage loading function with a custom path
    load_subpage(f"flyersub.{subpage}", subpage, flyer_pages)
