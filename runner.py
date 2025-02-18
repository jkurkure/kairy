#!/usr/bin/env python3.11
import subprocess, env

s = subprocess.Popen([env.PYRUNNER, 'App.pyw'], stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

print(f'{env.APP_NAME} is launched')

while True:
    output = s.stdout.readline() # type: ignore
    if output == '' and s.poll() is not None:
        break
    if output:
        print(output.strip())