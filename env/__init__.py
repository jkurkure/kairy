import subprocess, pickle, sys

PYRUNNER = sys.executable
REPO_NAME = "kairy"
APP_NAME = "Bringka"
APP_VERSION = f'{subprocess.Popen("git rev-parse --short HEAD", shell=True, stdout=subprocess.PIPE).communicate()[0]}'[
    2:-3
]

def secret(name):
    SECRET_PATH = "/home/private/.secrets"
    with open(SECRET_PATH, "rb") as f:
        return pickle.load(f)[name]
