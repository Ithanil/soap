import sqlite3
import argparse
import datetime
import matplotlib.pyplot as plt

argp = argparse.ArgumentParser()
argp.add_argument('-db', '--database', type=str, default="test.db", help='database file name')
args = argp.parse_args()

connection = sqlite3.connect(args.database)
cursor = connection.cursor()


# --- extract data from database ---
cursor.execute("SELECT * FROM transactions ORDER BY valutaDate ASC") 
result = cursor.fetchall()

change_dates = []
changes = []
for it, r in enumerate(result):
    dsplit = (r[3]).split('-')
    change_dates.append(datetime.date(int(dsplit[0]), int(dsplit[1]), int(dsplit[2])))
    changes.append(r[12])

print(change_dates)
print(changes)

# --- process data for plotting ---

dayincrement = datetime.timedelta(1)
nchanges = len(change_dates)
print(nchanges)
ndays = (change_dates[nchanges-1] - change_dates[0]).days
print(ndays)
currentDate = change_dates[0]
currentBalance = 0.0
dates = []
balances = []

ichange = 0
for iday in range(ndays):
    dates.append(change_dates[0] + iday * dayincrement)
    while dates[iday]>=change_dates[ichange]:
        currentBalance += changes[ichange]
        ichange += 1
    balances.append(currentBalance)

print(dates)
print(balances)

connection.close()

plt.plot(dates, balances)
plt.show()
