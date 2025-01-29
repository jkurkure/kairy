import platformdirs, pickle, os

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
    

def getTable(name, *columns):
    if name in MainDatabase:
        return MainDatabase[name]
    
    else:
        MainDatabase[name] = {}
        for col in columns:
            MainDatabase[name][col] = []

        with open(file_path, "wb") as f:
            pickle.dump(MainDatabase, f)

def addRow(tableName, **items):
    if tableName in MainDatabase:
        for col in MainDatabase[tableName]:
            if col in items:
                MainDatabase[tableName][col].append(items[col])
            else:
                MainDatabase[tableName][col].append(None)

        with open(file_path, "wb") as f:
                pickle.dump(MainDatabase, f)

def delRow(tableName, field, value):
    if tableName in MainDatabase:
        table = MainDatabase[tableName]
        for i, x in table[field]:
            if x == value:
                for col in table[col]:
                    pass