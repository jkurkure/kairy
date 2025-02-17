#!/usr/bin/env python3.11
from nicegui import ui

# Define the HTML and JavaScript for the button and window opening logic
html_content = """
<div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <button onclick="openWindow()" style="padding: 10px 20px; font-size: 16px;">
        Open Window
    </button>
</div>

<script>
function openWindow() {
    var newWindow = window.open('https://us-west.on-air.io/bringka/device-0/', '_blank', 'width=800,height=600');
    newWindow.onload = function() {
        newWindow.document.documentElement.style.overflow = 'hidden';  // Hide scrollbars
        newWindow.document.body.style.margin = '0';  // Remove margin
        newWindow.document.body.style.padding = '0';  // Remove padding
        newWindow.document.body.style.height = '100%';  // Full height
        newWindow.document.body.style.width = '100%';  // Full width
        newWindow.document.body.style.position = 'fixed';  // Prevent scrolling
    };
}
</script>
"""

# Use ui.html to render the custom HTML
ui.add_body_html(html_content)

ui.run()