import urllib.request
import sqlite3

def run_tests():
    conn = sqlite3.connect('ielts_platform.db')
    c = conn.cursor()
    c.execute("SELECT id, section_number, test_type, title FROM questions WHERE skill='Writing'")
    rows = c.fetchall()
    print("Total Writing Questions in DB:", len(rows))

    t1_id = None
    t2_id = None
    for row in rows:
        if row[1] == 1 and not t1_id:
            t1_id = row[0]
        elif row[1] == 2 and not t2_id:
            t2_id = row[0]

    print(f"Using Task 1 ID: {t1_id}, Task 2 ID: {t2_id}")

    # 1. Test Task 1 Single Mode
    res_t1 = urllib.request.urlopen(f'http://127.0.0.1:8000/writing-practice?id={t1_id}')
    html_t1 = res_t1.read().decode('utf-8')
    print("\n--- TEST 1: Task 1 Single Mode ---")
    print("Status:", res_t1.status)
    print("Timer 1200s (20 mins):", 'var timeRemaining = 1200;' in html_t1)
    print("Only Task 1 tab rendered:", ('id="taskTab1"' in html_t1 and 'id="taskTab2"' not in html_t1))
    print("Switch Task button hidden:", ('Switch to Task' not in html_t1))

    # 2. Test Task 2 Single Mode
    res_t2 = urllib.request.urlopen(f'http://127.0.0.1:8000/writing-practice?id={t2_id}')
    html_t2 = res_t2.read().decode('utf-8')
    print("\n--- TEST 2: Task 2 Single Mode ---")
    print("Status:", res_t2.status)
    print("Timer 2400s (40 mins):", 'var timeRemaining = 2400;' in html_t2)
    print("Only Task 2 tab rendered:", ('id="taskTab2"' in html_t2 and 'id="taskTab1"' not in html_t2))
    print("Switch Task button hidden:", ('Switch to Task' not in html_t2))

    # 3. Test Full Exam Mode (both tasks)
    res_full = urllib.request.urlopen(f'http://127.0.0.1:8000/writing-practice?t1_id={t1_id}&t2_id={t2_id}')
    html_full = res_full.read().decode('utf-8')
    print("\n--- TEST 3: Full Exam Mode (Both Tasks) ---")
    print("Status:", res_full.status)
    print("Timer 3600s (60 mins):", 'var timeRemaining = 3600;' in html_full)
    print("Both Task 1 & 2 tabs rendered:", ('id="taskTab1"' in html_full and 'id="taskTab2"' in html_full))
    print("Switch Task button visible:", ('Switch to Task' in html_full))

if __name__ == '__main__':
    run_tests()
