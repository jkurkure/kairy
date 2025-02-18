#!/usr/bin/env python3.11
import subprocess, env
s = subprocess.Popen(['python3.11', '/home/public/kairy/App.pyw'],stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,  # needed for the next line to be sensible
    stderr=subprocess.STDOUT)
print(f'{env.APP_NAME} is launched')

while True:
    try:
        line = s.stdout.readline().decode('utf-8').strip() # type: ignore
        if line == '':
            break
        print(line)
    except KeyboardInterrupt:
        break