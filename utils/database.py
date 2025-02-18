import platformdirs, pickle, os
import pandas as pd
from nicegui import ui

pd.options.display.float_format = "{:.0f}".format

data_dir = platformdirs.user_data_dir(appname="app", appauthor="kairy")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
file_path = os.path.join(data_dir, "kairy.database")


def saveDB():
    with open(file_path, "wb") as f:
        pickle.dump(MainDatabase, f)


if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        MainDatabase = pickle.load(f)
else:
    MainDatabase = {}
    open(file_path, "x")
    saveDB()

# def getTable(name, *columns):
#     if name in MainDatabase:
#         return MainDatabase[name]

#     else:
#         MainDatabase[name] = {}
#         for col in columns:
#             MainDatabase[name][col] = []

#         with open(file_path, "wb") as f:
#             pickle.dump(MainDatabase, f)

# def addRow(tableName, **items):
#     if tableName in MainDatabase:
#         for col in MainDatabase[tableName]:
#             if col in items:
#                 MainDatabase[tableName][col].append(items[col])
#             else:
#                 MainDatabase[tableName][col].append(None)

#         with open(file_path, "wb") as f:
#                 pickle.dump(MainDatabase, f)

# def delRow(tableName, field, value):
#     if tableName in MainDatabase:
#         table = MainDatabase[tableName]
#         for i, x in table[field]:
#             if x == value:
#                 for col in table[col]:
#                     pass


def newTable(name, *columns):
    if name not in MainDatabase:
        MainDatabase[name] = pd.DataFrame(columns=columns)
        saveDB()


def getTable(name):
    if name in MainDatabase:
        return MainDatabase[name]
    else:
        return None


def delTable(name):
    if name in MainDatabase:
        del MainDatabase[name]
        saveDB()


def addRow(tableName, *items):
    MainDatabase[tableName].loc[len(MainDatabase[tableName])] = items
    saveDB()


def delRow(tableName, field, value):
    MainDatabase[tableName] = MainDatabase[tableName][
        MainDatabase[tableName][field] != value
    ]
    saveDB()


def updateRow(tableName, searchField, searchValue, targetField, newValue):
    MainDatabase[tableName].loc[
        MainDatabase[tableName][searchField] == searchValue, targetField
    ] = newValue
    saveDB()


def getRow(tableName, field, value):
    return (
        MainDatabase[tableName].index[query := MainDatabase[tableName][field] == value],
        MainDatabase[tableName][query],
    )


def hasCell(tableName, field, value):
    return len(getRow(tableName, field, value)[0]) > 0


def showTable(tableName):
    ui.table.from_pandas(getTable(tableName)).classes("w-full")  # type: ignore
