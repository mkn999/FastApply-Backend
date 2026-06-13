import sqlite3

conn = sqlite3.connect("jobs.db")

cursor = conn.cursor() #used to write things in data

# cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (
#     id INTEGER PRIMARY KEY,
#     title TEXT,
#     company TEXT
#     )""")

# cursor.execute("""INSERT INTO jobs (title,company) VALUES('Software Engineer','Kerala Startup Mission')""") #add another row , doesnt replace row

cursor.execute("SELECT * from jobs") #give all columns from jobs table
rows = cursor.fetchall() #get all result returned by query , (fetchone(),fetchmany(2)[fetches first 2 rows])
print(rows)

# conn.commit()
