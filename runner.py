#!/usr/bin/env python3.11
import subprocess, env
subprocess.Popen(['python3.11', '/home/public/kairy/App.pyw'],stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,  # needed for the next line to be sensible
    stderr=subprocess.STDOUT)
print(f'{env.APP_NAME} is launched')