import sqlite3
import json

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

reading_qs = cursor.execute("SELECT id, title, question_type, passage_or_context, options_json FROM questions WHERE skill = 'Reading'").fetchall()
print(f"Total Reading questions in DB: {len(reading_qs)}")

passages = {}
for q in reading_qs:
    t = q['title']
    if t not in passages:
        passages[t] = []
    passages[t].append(q)

for title, qs in passages.items():
    print(f"\nPassage Title: '{title}' ({len(qs)} questions)")
    for q in qs[:3]:
        print(f"  Q{q['id']}: [{q['question_type']}] len(passage)={len(q['passage_or_context'])} opts={q['options_json']}")
