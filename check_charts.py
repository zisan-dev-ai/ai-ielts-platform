import sqlite3
conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check first Task 1 question loaded by default
c.execute("SELECT id, title, question_type FROM questions WHERE skill = 'Writing' AND section_number = 1 ORDER BY id LIMIT 1")
r = c.fetchone()
print(f"Default Task 1: ID={r['id']} | {r['title']} | {r['question_type']}")

# Check the passage_or_context has SVG
c.execute("SELECT passage_or_context FROM questions WHERE id = ?", (r['id'],))
ctx = c.fetchone()['passage_or_context']
has_svg = '<svg' in ctx if ctx else False
print(f"Has SVG: {has_svg}")
print(f"Context length: {len(ctx)} chars")
print(f"First 500 chars of context:\n{ctx[:500]}")

# Check first Task 2
c.execute("SELECT id, title, question_type FROM questions WHERE skill = 'Writing' AND (section_number = 2 OR test_type LIKE '%Task 2%') ORDER BY id LIMIT 1")
r2 = c.fetchone()
print(f"\nDefault Task 2: ID={r2['id']} | {r2['title']} | {r2['question_type']}")

conn.close()
