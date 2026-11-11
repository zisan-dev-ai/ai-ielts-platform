import sqlite3
import json
import requests
import time

conn = sqlite3.connect('ielts_platform.db')
conn.row_factory = sqlite3.Row
row = conn.cursor().execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'gemini' AND status = 'Active' LIMIT 1").fetchone()
key = row['api_key']

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse&key={key}"
payload = {
    "contents": [{"parts": [{"text": "Say hello in 5 words."}]}]
}

start = time.time()
r = requests.post(url, json=payload, stream=True, timeout=10)
first_token_time = None

for line in r.iter_lines():
    if line:
        decoded = line.decode('utf-8')
        if decoded.startswith('data: '):
            if first_token_time is None:
                first_token_time = time.time() - start
                print(f"First chunk arrived in: {first_token_time:.2f} seconds!")
            data = json.loads(decoded[6:])
            text = data['candidates'][0]['content']['parts'][0]['text']
            print(text, end="", flush=True)

total_time = time.time() - start
print(f"\nTotal stream completed in: {total_time:.2f} seconds!")
