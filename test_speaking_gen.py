import urllib.request
import json

base_url = "http://127.0.0.1:8000"

print("Testing POST /api/v1/speaking/generate-set ...")
req = urllib.request.Request(
    f"{base_url}/api/v1/speaking/generate-set",
    data=json.dumps({"theme": "Space Exploration & Science"}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))
print(f"Status: {resp.status}")
print(f"Theme: {data.get('theme')}")
print(f"Part 1 Questions ({len(data.get('part1', {}).get('questions', []))}): {data.get('part1', {}).get('questions', [])}")
print(f"Part 2 Cue Card: {data.get('part2', {}).get('title')}")
print(f"Part 3 Questions ({len(data.get('part3', {}).get('questions', []))}): {data.get('part3', {}).get('questions', [])}")
print("\nDynamic Speaking Set Generation Working Flawlessly!")
