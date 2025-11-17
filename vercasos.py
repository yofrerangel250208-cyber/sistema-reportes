import sqlite3

conn = sqlite3.connect("casos.db")
c = conn.cursor()

c.execute("SELECT * FROM casos")
for fila in c.fetchall():
    print(fila)

conn.close()
