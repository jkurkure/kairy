#!/usr/bin/env python3.11
import subprocess, env, time

s = subprocess.Popen([env.PYRUNNER, 'App.pyw'], stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

print(f'{env.APP_NAME} is launched')

while True:
    print(f'Still alive at {time.ctime()}')

    output = s.stdout.readline() # type: ignore
    if output == '' and s.poll() is not None:
        time.sleep(0.1)
    if output:
        print(output.strip())