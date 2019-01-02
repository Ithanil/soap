import sqlite3
import argparse

argp = argparse.ArgumentParser()
argp.add_argument('-db', '--database', type=str, default="test.db", help='database file name')
args = argp.parse_args()

connection = sqlite3.connect(args.database)
cursor = connection.cursor()

cursor.execute("SELECT * FROM transactions") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)

connection.close()
