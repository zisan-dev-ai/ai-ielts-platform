import sqlite3
import re

def fix_writing_contrast():
    # 1. Update SQLite DB
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, passage_or_context FROM questions WHERE skill = 'Writing'")
    rows = cursor.fetchall()
    updated = 0
    for qid, ctx in rows:
        if ctx and ('color:#fff' in ctx or 'color: #fff' in ctx or 'rgba(225,29,72,0.1)' in ctx or 'rgba(225, 29, 72, 0.1)' in ctx):
            new_ctx = re.sub(r'style="[^"]*background:\s*rgba\(225,\s*29,\s*72,\s*0\.1\)[^"]*"', 'class="prompt-statement-highlight"', ctx)
            new_ctx = new_ctx.replace('color:#fff;', '').replace('color: #fff;', '').replace('color:#fff', '').replace('color: #fff', '')
            cursor.execute('UPDATE questions SET passage_or_context = ? WHERE id = ?', (new_ctx, qid))
            updated += 1
    conn.commit()
    conn.close()
    print(f"SUCCESS: Updated {updated} writing tasks in DB for 100% crystal clear contrast in Light & Dark modes.")

    # 2. Update seed_authentic_cambridge_writing_full.py
    with open('seed_authentic_cambridge_writing_full.py', 'r', encoding='utf-8') as f:
        code = f.read()

    code = re.sub(r'style="background:rgba\(225,29,72,0\.1\);[^"]*color:#fff;[^"]*"', 'class="prompt-statement-highlight"', code)
    
    with open('seed_authentic_cambridge_writing_full.py', 'w', encoding='utf-8') as f:
        f.write(code)

    print("SUCCESS: Updated seed_authentic_cambridge_writing_full.py.")

if __name__ == '__main__':
    fix_writing_contrast()
