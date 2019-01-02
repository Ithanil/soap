import sqlite3
import csv
import hashlib

connection = sqlite3.connect("transactions.db")

cursor = connection.cursor()

# delete 
#cursor.execute("""DROP TABLE transactions;""")

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

statementFile = open('test.csv')
reader = csv.reader(statementFile, delimiter=';')
for count, row in enumerate(reader):
    print(row)
    if count < 1:
        continue
    sql_command = """INSERT INTO transactions 
    (hash, accountID, postingDate, valutaDate, postingText, referenceText, creditorID, mandateRef, customerRef, targetName, targetIBAN, targetBIC, amount, currency) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    try:
        rawText = ';'.join(row)
        hash = hashlib.sha256(rawText.encode('utf-8')).hexdigest()
        cursor.execute(sql_command, (hash, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[11], row[12], row[13], row[14], row[15]))
    except Exception as e:
        print("Warning: A transaction could not be inserted into the database.")
        print(e)

# never forget this, if you want the changes to be saved:
connection.commit()

cursor.execute("SELECT * FROM transactions") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("SELECT * FROM transactions")
print("\nfetch one:")
res = cursor.fetchone() 
print(res)

connection.close()
