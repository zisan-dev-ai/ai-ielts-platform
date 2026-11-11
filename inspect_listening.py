import sqlite3

conn = sqlite3.connect('ielts_platform.db')
c = conn.cursor()
c.execute("SELECT section_number, id, question_type, title, question_text, answer_key FROM questions WHERE skill = 'Listening' ORDER BY id ASC")
rows = c.fetchall()
print(f"Total listening questions: {len(rows)}")
for r in rows:
    print(f"Sec {r[0]} | Q{r[1]} | Type: {r[2]:20} | Text: {r[4][:40]} | Ans: {r[5]}")
conn.close()
