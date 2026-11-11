import sqlite3
conn = sqlite3.connect('ielts_platform.db')
c = conn.cursor()
c.execute("UPDATE ai_credentials SET status='Active', error_count=0")
conn.commit()
conn.close()
print('Reset complete.')