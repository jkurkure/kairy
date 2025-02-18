#!/usr/bin/env python3.11
import subprocess, env, time, random

pop = subprocess.Popen([env.PYRUNNER, 'App.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(f'{env.APP_NAME} is launched')

while pop.poll() is None:
    time.sleep(random.uniform(1/50, 2))
    print(f'{env.APP_NAME} is running at {time.ctime()}')
    output = pop.stdout.readline()
    if output:
        print(output.strip())
    error = pop.stderr.readline()
    if error:
        print(f'Error: {error.strip()}')

else:
    print(f'{env.APP_NAME} is terminated')