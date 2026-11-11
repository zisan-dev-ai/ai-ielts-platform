import urllib.request
import json

def test_ai_help_endpoints():
    base = "http://127.0.0.1:8000"
    
    # 1. Test Writing Page HTML
    res = urllib.request.urlopen(f"{base}/writing-practice")
    html = res.read().decode('utf-8')
    print("Writing Page Status:", res.status)
    print("AI Help Button Present:", "bc-btn-ai-help" in html)
    print("AI Help Drawer Present:", "id=\"aiHelpDrawer\"" in html)
    print("Floating Polish Btn Present:", "id=\"floatingPolishBtn\"" in html)

    # 2. Test Brainstorm API
    req = urllib.request.Request(
        f"{base}/api/v1/writing/ai-help/brainstorm",
        data=json.dumps({
            "task_type": "Task 2 - Agree or Disagree",
            "prompt_title": "AI & Future Employment",
            "prompt_statement": "Some people believe that artificial intelligence will create more jobs than it destroys."
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    b_res = urllib.request.urlopen(req)
    b_data = json.loads(b_res.read().decode('utf-8'))
    print("\n--- BRAINSTORM API ---")
    print("Status:", b_res.status)
    print("Has key_points_group_a:", "key_points_group_a" in b_data.get("data", {}))

    # 3. Test Vocabulary API
    req_v = urllib.request.Request(
        f"{base}/api/v1/writing/ai-help/vocabulary",
        data=json.dumps({
            "task_type": "Task 2 - Agree or Disagree",
            "prompt_title": "AI & Future Employment",
            "prompt_statement": "Some people believe that artificial intelligence will create more jobs than it destroys."
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    v_res = urllib.request.urlopen(req_v)
    v_data = json.loads(v_res.read().decode('utf-8'))
    print("\n--- VOCABULARY API ---")
    print("Status:", v_res.status)
    print("Has topic_collocations:", "topic_collocations" in v_data.get("data", {}))

    # 4. Test Polish Sentence API
    req_p = urllib.request.Request(
        f"{base}/api/v1/writing/ai-help/polish-sentence",
        data=json.dumps({
            "sentence": "AI makes people lose their jobs and this is bad for society.",
            "task_type": "Task 2"
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    p_res = urllib.request.urlopen(req_p)
    p_data = json.loads(p_res.read().decode('utf-8'))
    print("\n--- POLISH SENTENCE API ---")
    print("Status:", p_res.status)
    print("Band 8.5 Version:", p_data.get("data", {}).get("band_8_version"))

if __name__ == '__main__':
    test_ai_help_endpoints()
