import sqlite3
import json
import requests

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
row = conn.cursor().execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'grok' AND status = 'Active' LIMIT 1").fetchone()
if row:
    key = row['api_key']
    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    models = ["grok-3-mini", "grok-2-latest", "grok-beta"]
    for m in models:
        try:
            res = requests.post(url, headers=headers, json={"model": m, "messages": [{"role": "user", "content": "Hello"}]}, timeout=15)
            print(f"Grok {m} status:", res.status_code, res.text[:100])
        except Exception as e:
            print(f"Grok {m} error:", e)
else:
    print("No active Grok key found")
