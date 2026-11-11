import sqlite3
import urllib.request
import json

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
row = conn.cursor().execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'gemini' AND status = 'Active' LIMIT 1").fetchone()
if row:
    key = row['api_key']
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        req = urllib.request.Request(url)
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        models = [m['name'].replace('models/', '') for m in res.get('models', [])]
        print("Supported Gemini Models:")
        for m in sorted(models):
            if 'gemini' in m:
                print(" -", m)
    except Exception as e:
        print("API error:", e)
else:
    print("No active Gemini key found.")
