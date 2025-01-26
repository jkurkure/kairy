import random, sys, platformdirs, pickle, os

data_dir = platformdirs.user_data_dir(
    appname="app",
    appauthor="kairy")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
file_path = os.path.join(data_dir, "main.database")

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        MainDatabase = pickle.load(f)
else:
    MainDatabase = {}
    open(file_path, "x")
    

def Table(name, *columns):
    if name in MainDatabase:
        return MainDatabase[name]
    
    else:
        MainDatabase[name] = {}
        for col in columns:
            MainDatabase[name][col] = []

        with open(file_path, "wb") as f:
            pickle.dump(MainDatabase, f)