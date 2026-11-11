import urllib.request
import json

base_url = "http://127.0.0.1:8000"

print("1. Testing GET /speaking-practice ...")
resp1 = urllib.request.urlopen(f"{base_url}/speaking-practice")
print(f"   Status: {resp1.status} (Length: {len(resp1.read())} bytes)")

print("\n2. Testing GET /practice ...")
resp2 = urllib.request.urlopen(f"{base_url}/practice")
print(f"   Status: {resp2.status} (Length: {len(resp2.read())} bytes)")

print("\n3. Testing POST /api/v1/speaking/evaluate ...")
req3 = urllib.request.Request(
    f"{base_url}/api/v1/speaking/evaluate",
    data=json.dumps({
        "user_id": 1,
        "part_number": 1,
        "prompt_title": "Speaking Mock Part 1",
        "prompt_text": "Hometown & Work",
        "transcript": "I live in Chittagong, which is a large coastal city. I have been working as a software engineer for three years, and I really enjoy developing innovative solutions.",
        "time_spent_seconds": 60
    }).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
resp3 = urllib.request.urlopen(req3)
eval_data = json.loads(resp3.read().decode('utf-8'))
print(f"   Status: {resp3.status}")
print(f"   Overall Band: {eval_data.get('overall_band')}")
print(f"   FC: {eval_data.get('fluency_coherence')}, LR: {eval_data.get('lexical_resource')}, GRA: {eval_data.get('grammatical_range')}, PR: {eval_data.get('pronunciation')}")
print(f"   Strengths: {eval_data.get('strengths')}")

print("\nAll endpoints verified successfully!")
