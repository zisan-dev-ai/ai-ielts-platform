import sqlite3
import urllib.request
import json

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
row = conn.cursor().execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'gemini' AND status = 'Active' LIMIT 1").fetchone()
key = row['api_key']

models_to_test = ["gemini-3.7-flash", "gemini-2.5-flash", "gemini-2.5-pro"]

for model in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, explain the difference between 'few' and 'a few' in 1 sentence."}]
        }]
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        text = res['candidates'][0]['content']['parts'][0]['text']
        print(f"[SUCCESS] {model}: {text.strip()[:100]}")
    except Exception as e:
        print(f"[FAILED] {model}:", e)
