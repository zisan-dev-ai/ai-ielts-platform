import sqlite3, json

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT * FROM questions WHERE skill = 'Speaking' LIMIT 3")
for r in c.fetchall():
    print(dict(r))

conn.close()
