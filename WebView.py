#!/usr/bin/env python3.11
from nicegui import ui
import env

# Define the HTML and JavaScript for the button and window opening logic
html_content = f'''
<div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <button onclick="openWindow()" style="padding: 10px 20px; font-size: 16px;">
        Open {env.APP_NAME} in Browser
    </button>

    <button onclick="openWindow()" style="padding: 10px 20px; font-size: 16px;">
        Get {env.APP_NAME} from Play Store
    </button>
</div>
'''

js_content = """
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
# Add javascript to page
ui.add_head_html(js_content)
# Render custom html into page
ui.add_body_html(html_content)

ui.run()