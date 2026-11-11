from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def run_tests():
    print("Testing /api/v1/practice/submit-objective...")
    # First, let's submit a correct answer for Reading MCQ
    # In seed_data.py, first reading question has ID 22 (21 listening questions before it)
    response = client.post(
        "/api/v1/practice/submit-objective",
        json={
            "question_id": 22,
            "user_answer": "Sample Answer",
            "time_taken_seconds": 15
        }
    )
    print("Response Status:", response.status_code)
    print("Response Body:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    run_tests()