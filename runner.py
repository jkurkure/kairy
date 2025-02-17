import subprocess
subprocess.Popen(['python3.11', '/home/public/kairy/App.pyw'],stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,  # needed for the next line to be sensible
    stderr=subprocess.STDOUT)
print('Bringka is launched')