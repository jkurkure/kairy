#!/usr/bin/env python3.11
import subprocess
from nicegui import ui
subprocess.Popen(['python3.11', '/home/public/kairy/App.pyw'])
ui.label('Bringka has been launched')
ui.run(port=8090, dark=True)