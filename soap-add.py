import sqlite3
import csv
import hashlib
import argparse

argp = argparse.ArgumentParser()
argp.add_argument('-i', '--input', type=str, default="test.csv", help='input file name')
argp.add_argument('-db', '--database', type=str, default="test.db", help='database file name')
args = argp.parse_args()

# --- open database and create table if not existant ---
connection = sqlite3.connect(args.database)
cursor = connection.cursor()

sql_command = """
CREATE TABLE IF NOT EXISTS transactions ( 
hash TEXT NOT NULL UNIQUE,
accountID TEXT,
postingDate DATE,
valutaDate DATE,
postingText TEXT,
referenceText TEXT, 
creditorID TEXT,
mandateRef TEXT,
customerRef TEXT,
targetName TEXT,
targetIBAN TEXT,
targetBIC TEXT,
amount REAL,
currency TEXT);"""

cursor.execute(sql_command)


# --- parse statement file and fill database ---
statementFile = open(args.input)
reader = csv.reader(statementFile, delimiter=';')

for count, row in enumerate(reader):
    #print(row)
    if count < 1: # skip header
        continue
    sql_command = """INSERT INTO transactions 
    (hash, accountID, postingDate, valutaDate, postingText, referenceText, creditorID, mandateRef, customerRef, targetName, targetIBAN, targetBIC, amount, currency) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    try:
        rawText = ';'.join(row)
        hash = hashlib.sha256(rawText.encode('utf-8')).hexdigest()

        # the following contains code specific to german bank statements (date format, comma in floats)
        dates = []
        for dateRow in [row[1], row[2]]:
            dateSplit = dateRow.split('.')
            dates.append('20' + dateSplit[2] + '-' + dateSplit[1] + '-' + dateSplit[0])
        cursor.execute(sql_command, (hash, row[0], dates[0], dates[1], row[3], row[4], row[5], row[6], row[7], row[11], row[12], row[13], float(row[14].replace(',','.')), row[15]))
    except Exception as e:
        print("Warning: A transaction could not be inserted into the database.")
        print(e)


# --- save changes and close ---
connection.commit()
connection.close()
