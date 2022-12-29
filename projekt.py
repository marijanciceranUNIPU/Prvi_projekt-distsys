import sqlite3

conn = sqlite3.connect('dbase.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM mini_projekt_db")
counter_check = cursor.fetchone()[0]

if counter_check == 0:
    print("Database is empty.")
else:
    print("Database is NOT empty.")

query = 'SELECT id, username, ghublink, filename FROM mini_projekt_db'

results = cursor.execute(query)

for row in results:
    print(row)

conn.close()