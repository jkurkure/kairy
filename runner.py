#!/usr/bin/env python3.11
import subprocess, env, time, random

pop = subprocess.Popen([env.PYRUNNER, 'App.pyw'])
print(f'{env.APP_NAME} is launched')

while pop.poll() is None:
    time.sleep(random.uniform(1/50, 2))
    print(f'{env.APP_NAME} is running at {time.ctime()}')

else:
    print(f'{env.APP_NAME} is terminated')



# while True:
#     print(f'Still alive at {time.ctime()}')

#     output = s.stdout.readline() # type: ignore
#     if output == '' and s.poll() is not None:
#         time.sleep(0.1)
#     if output:
#         print(output.strip())