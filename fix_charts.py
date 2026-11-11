"""
Fix script: Delete AI-generated Task 1 writing questions with bad charts
and verify seeded questions are intact.
"""
import sqlite3

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Delete ALL AI-generated Task 1 questions (their charts are all low quality)
c.execute("SELECT id, title FROM questions WHERE skill = 'Writing' AND section_number = 1 AND cambridge_book = 'AI Generated Custom'")
ai_task1 = c.fetchall()
print(f"Found {len(ai_task1)} AI-generated Task 1 questions to delete:")
for r in ai_task1:
    print(f"  Deleting ID={r['id']}: {r['title']}")

c.execute("DELETE FROM questions WHERE skill = 'Writing' AND section_number = 1 AND cambridge_book = 'AI Generated Custom'")
deleted = c.rowcount
print(f"\nDeleted {deleted} bad AI-generated Task 1 questions.")

# Verify seeded Task 1 questions remain
c.execute("SELECT id, title, cambridge_book FROM questions WHERE skill = 'Writing' AND section_number = 1 ORDER BY id")
remaining = c.fetchall()
print(f"\nRemaining Task 1 questions ({len(remaining)}):")
for r in remaining:
    print(f"  ID={r['id']} | {r['title'][:60]} | {r['cambridge_book']}")

# Also check Task 2
c.execute("SELECT id, title, cambridge_book FROM questions WHERE skill = 'Writing' AND section_number = 2 ORDER BY id")
task2 = c.fetchall()
print(f"\nTask 2 questions ({len(task2)}):")
for r in task2:
    print(f"  ID={r['id']} | {r['title'][:60]} | {r['cambridge_book']}")

conn.commit()
conn.close()
print("\nDone! Bad charts removed.")
