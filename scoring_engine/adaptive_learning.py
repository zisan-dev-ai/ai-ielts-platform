import json
from database import get_db

class AdaptiveLearningEngine:
    @staticmethod
    def record_mistake(user_id: int, skill: str, q_type: str, title: str, user_ans: str, correct_ans: str, explanation: str):
        """Automatically saves a wrong answer to the user's Mistake Notebook."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mistake_notebook 
            (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, skill, q_type, title, user_ans, correct_ans, explanation))

        # Update Skill Mastery
        cursor.execute("""
            INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, mastery_percentage)
            VALUES (?, ?, ?, 1, 0, 0.0)
            ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
            total_attempted = total_attempted + 1,
            mastery_percentage = (total_correct * 100.0) / (total_attempted + 1),
            last_updated = CURRENT_TIMESTAMP
        """, (user_id, skill, q_type))

        conn.commit()
        conn.close()

    @staticmethod
    def record_correct_answer(user_id: int, skill: str, q_type: str):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, mastery_percentage)
            VALUES (?, ?, ?, 1, 1, 100.0)
            ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
            total_attempted = total_attempted + 1,
            total_correct = total_correct + 1,
            mastery_percentage = ((total_correct + 1) * 100.0) / (total_attempted + 1),
            last_updated = CURRENT_TIMESTAMP
        """, (user_id, skill, q_type))
        conn.commit()
        conn.close()

    @staticmethod
    def build_tailored_tasks(target_band: float, mins: int, weak_type: str = None) -> list:
        # Default weak type if none recorded yet
        if not weak_type:
            if target_band >= 8.0:
                weak_type = "Yes / No / Not Given & Inferences"
            elif target_band >= 7.0:
                weak_type = "True / False / Not Given"
            else:
                weak_type = "Sentence Completion & Multiple Choice"

        tasks = []

        # BAND 6.0 - 6.5 (Foundational & Competent Target)
        if target_band <= 6.5:
            if mins <= 30:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "15 Mins",
                        "title": f"Reading Drill: {weak_type}",
                        "desc": "বেসিক প্রশ্ন ফরম্যাট বুঝে মনোযোগ দিয়ে ৫টি প্রশ্নের সঠিক উত্তর সমাধান করুন।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "15 Mins",
                        "title": "Grammar: Subject-Verb & Tenses",
                        "desc": "সহজ ব্যাকরণ ও নিয়মিত ভুলের জায়গাগুলো বুঝে বাক্য গঠন শুদ্ধ করুন।",
                        "url": "/grammar",
                        "btn_text": "Open Rules →"
                    }
                ]
            elif mins <= 45:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "15 Mins",
                        "title": f"Reading Trap Drill: {weak_type}",
                        "desc": "প্যাসেজের সহজ টেকনিক ব্যবহার করে বিভ্রান্তিকর অপশন পরিহারের অনুশীলন।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "15 Mins",
                        "title": "Grammar: Articles & Prepositions",
                        "desc": "অ্যাকাডেমিক বাক্যে সঠিক প্রিপজিশন ও আর্টিকেল ব্যবহারের মৌলিক নিয়মাবলি।",
                        "url": "/grammar",
                        "btn_text": "Open Rules →"
                    },
                    {
                        "step": 3,
                        "time_badge": "15 Mins",
                        "title": "Speaking Part 1 Everyday Topics",
                        "desc": "এআই শিক্ষকের সাথে দৈনন্দিন সাধারণ বিষয়ে জড়তাহীন স্পষ্ট উচ্চারণে কথা বলুন।",
                        "url": "/ai-teacher",
                        "btn_text": "Talk to ARIA →"
                    }
                ]
            elif mins <= 60:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "20 Mins",
                        "title": f"Timed Reading Passage: {weak_type}",
                        "desc": "ঘড়ি ধরে ২০ মিনিটে নির্দিষ্ট প্যাসেজের প্রশ্নসমূহ নির্ভুলভাবে সমাধান করুন।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "20 Mins",
                        "title": "Grammar & Essential Vocabulary",
                        "desc": "Band 6.5 উপযোগী বাক্য গঠন এবং জরুরি অ্যাকাডেমিক শব্দভাণ্ডার অনুশীলন।",
                        "url": "/vocabulary",
                        "btn_text": "Master Vocab →"
                    },
                    {
                        "step": 3,
                        "time_badge": "20 Mins",
                        "title": "Speaking Part 1 & Part 2 Cue Card",
                        "desc": "কিউ কার্ডের সাধারণ পয়েন্টগুলো সুন্দরভাবে ২ মিনিটে গুছিয়ে বলার প্র্যাকটিস।",
                        "url": "/practice?skill=Speaking",
                        "btn_text": "Record Speech →"
                    }
                ]
            else:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "25 Mins",
                        "title": f"Comprehensive Reading Drill: {weak_type}",
                        "desc": "প্যাসেজ স্কিমিং ও স্ক্যানিং কৌশলের মাধ্যমে প্রশ্ন সমাধান ও ভুলের পর্যালোচনা।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "25 Mins",
                        "title": "Writing Task 1 Overview & Structure",
                        "desc": "টাস্ক ১ এর গ্রাফ/চার্ট বিশ্লেষণ ও স্পষ্ট ওভারভিউ লেখার নিয়ম ও উদাহরণ।",
                        "url": "/practice?skill=Writing",
                        "btn_text": "Practice Writing →"
                    },
                    {
                        "step": 3,
                        "time_badge": "20 Mins",
                        "title": "Grammar Master: Sentence Construction",
                        "desc": "কমপ্লেক্স ও কম্পাউন্ড বাক্যের বেসিক স্ট্রাকচার আয়ত্ত করুন।",
                        "url": "/grammar",
                        "btn_text": "Open Rules →"
                    },
                    {
                        "step": 4,
                        "time_badge": "20 Mins",
                        "title": "Speaking Practice Session with ARIA",
                        "desc": "এআই শিক্ষকের সাথে লাইভ স্পিকিং কথোপকথন করে তাৎক্ষণিক ব্যান্ড স্কোর যাচাই।",
                        "url": "/ai-teacher",
                        "btn_text": "Enter Classroom →"
                    }
                ]

        # BAND 7.0 - 7.5 (Academic Excellence / University Standard)
        elif target_band < 8.0:
            if mins <= 30:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "15 Mins",
                        "title": f"Trap Elimination Drill: {weak_type}",
                        "desc": "প্যারাফ্রেজিং এবং সূক্ষ্ম ডিসট্র্যাক্টর চিহ্নিত করে ৫টি অফিশিয়াল প্রশ্ন সমাধান।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "15 Mins",
                        "title": "Complex Sentences & High-Yield Lexicon",
                        "desc": "কন্ডিশনালস ও কমপ্লেক্স সেন্টেন্সের মাধ্যমে রাইটিং ও স্পিকিংয়ে Band 7.5+ ফ্লুয়েন্সি।",
                        "url": "/grammar",
                        "btn_text": "Open Rules →"
                    }
                ]
            elif mins <= 45:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "15 Mins",
                        "title": f"Core Strategy & Trap Drill: {weak_type}",
                        "desc": "প্যাসেজের জটিল ফাঁদসমূহ সমাধান ও সময় সাশ্রয়ী স্ক্যানিং টেকনিক।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "15 Mins",
                        "title": "Academic Lexicon & Collocations Upgrade",
                        "desc": "টপিক-ভিত্তিক হাই-ব্যান্ড কোলোকেশন ও অ্যাকাডেমিক বাক্যের বৈচিত্র্য ঝালাই।",
                        "url": "/vocabulary",
                        "btn_text": "Master Vocab →"
                    },
                    {
                        "step": 3,
                        "time_badge": "15 Mins",
                        "title": "Speaking Cue Card or Writing Task 2 Outline",
                        "desc": "২ মিনিটের কিউ কার্ড রেকর্ড অথবা টাস্ক ২ ইন্ট্রোডাকশন লিখে এআই এক্সামিনার ফিডব্যাক।",
                        "url": "/practice?skill=Speaking",
                        "btn_text": "Record Speech →"
                    }
                ]
            elif mins <= 60:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "20 Mins",
                        "title": f"Timed CBT Reading Passage: {weak_type}",
                        "desc": "২০ মিনিটে সম্পূর্ণ প্যাসেজ সমাধান করে অফিশিয়াল স্পিড ও অ্যাকুরেসি বজায় রাখুন।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Timed Passage →"
                    },
                    {
                        "step": 2,
                        "time_badge": "20 Mins",
                        "title": "Advanced Grammar: Passive & Conditionals",
                        "desc": "অ্যাকাডেমিক হেজিং ও কন্ডিশনালস দিয়ে রাইটিং টাস্ক ২ এর বাক্য উন্নত করুন।",
                        "url": "/grammar",
                        "btn_text": "Master Rules →"
                    },
                    {
                        "step": 3,
                        "time_badge": "20 Mins",
                        "title": "Live Spoken Mock Interview with ARIA",
                        "desc": "পার্ট ২ কিউ কার্ড ও পার্ট ৩ এর গভীর বিশ্লেষণী প্রশ্নের লাইভ মক সাক্ষাৎকার।",
                        "url": "/ai-teacher",
                        "btn_text": "Enter Classroom →"
                    }
                ]
            else:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "25 Mins",
                        "title": f"Intensive CBT Reading Section: {weak_type}",
                        "desc": "কেমব্রিজ অ্যাকাডেমিক রিডিং টেস্টের কঠিন প্রশ্নসমূহ সমাধান ও প্যারাফ্রেজিং ডিকোড।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "25 Mins",
                        "title": "Writing Task 2 Full Essay Draft & Evaluation",
                        "desc": "২৫০+ শব্দের প্রবন্ধ লিখে সাবমিট করুন এবং গ্রামার ও কোহেরেন্সের স্কোর নিন।",
                        "url": "/practice?skill=Writing",
                        "btn_text": "Write Essay →"
                    },
                    {
                        "step": 3,
                        "time_badge": "20 Mins",
                        "title": "C1/C2 Academic Vocabulary Bank",
                        "desc": "শিক্ষা, অর্থনীতি ও পরিবেশের মতো মূল বিষয়ের উচ্চমানের শব্দভাণ্ডার আয়ত্ত করুন।",
                        "url": "/vocabulary",
                        "btn_text": "Master Vocab →"
                    },
                    {
                        "step": 4,
                        "time_badge": "20 Mins",
                        "title": "Speaking Part 2 & 3 Drill with ARIA",
                        "desc": "সাবলীল সাইনপোস্টিং ও প্রাকৃতিক বাচনভঙ্গির মাধ্যমে Band 7.5 স্পিকিং অর্জন।",
                        "url": "/ai-teacher",
                        "btn_text": "Start Speaking →"
                    }
                ]

        # BAND 8.0 - 9.0 (Elite Master / Top Score)
        else:
            if mins <= 30:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "15 Mins",
                        "title": f"Passage 3 Complex Inference: {weak_type}",
                        "desc": "অ্যাকাডেমিক দর্শনের গভীর প্যারাফ্রেজিং ও সূক্ষ্ম অর্থ উদ্ধার অনুশীলন।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "15 Mins",
                        "title": "Nominalization & Cleft Sentences (Band 9 GRA)",
                        "desc": "উচ্চমানের অ্যাকাডেমিক ডেনসিটি ও বাক্যের শৈল্পিক বৈচিত্র্য অনুশীলন।",
                        "url": "/grammar",
                        "btn_text": "Master Rules →"
                    }
                ]
            elif mins <= 45:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "15 Mins",
                        "title": f"Elite Trap Elimination: {weak_type}",
                        "desc": "কেমব্রিজ এক্সামিনার লেভেল বিভ্রান্তি শনাক্ত ও শতভাগ নির্ভুল উত্তর নিশ্চিতকরণ।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Start Drill →"
                    },
                    {
                        "step": 2,
                        "time_badge": "15 Mins",
                        "title": "Inversion & Participle Clauses for Band 8.5+",
                        "desc": "জটিল কিন্তু স্বাভাবিক অ্যাকাডেমিক এক্সপ্রেশন ও কোহিশনাল ডিভাইস মাস্টার করুন।",
                        "url": "/grammar",
                        "btn_text": "Master Rules →"
                    },
                    {
                        "step": 3,
                        "time_badge": "15 Mins",
                        "title": "Speaking Part 3 Societal Debates with ARIA",
                        "desc": "জটিল বিমূর্ত বিষয়ে সাবলীলভাবে উচ্চমানের চিন্তা ও যুক্তি উপস্থাপনের অনুশীলন।",
                        "url": "/ai-teacher",
                        "btn_text": "Debate with ARIA →"
                    }
                ]
            elif mins <= 60:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "20 Mins",
                        "title": f"High-Pressure Speed Reading Passage 3",
                        "desc": "কঠিনতম অ্যাকাডেমিক অনুচ্ছেদ নিখুঁত টাইম ম্যানেজমেন্টের মাধ্যমে সমাধান।",
                        "url": f"/practice?skill=Reading&q_type={weak_type.replace(' ', '+')}",
                        "btn_text": "Timed Passage →"
                    },
                    {
                        "step": 2,
                        "time_badge": "20 Mins",
                        "title": "Band 8.5+ Academic Lexical Precision",
                        "desc": "বিরল কিন্তু প্রাসঙ্গিক অ্যাকাডেমিক শব্দভাণ্ডার ও ইডিয়মেটিক ন্যাচারালনেস।",
                        "url": "/vocabulary",
                        "btn_text": "Master Vocab →"
                    },
                    {
                        "step": 3,
                        "time_badge": "20 Mins",
                        "title": "Full Speaking Test with Senior Examiner",
                        "desc": "ARIA-র সাথে ৩টি অংশেরই সম্পূর্ণ পরীক্ষা দিয়ে ব্যান্ড ৮.৫+ ফ্লুয়েন্সি যাচাই।",
                        "url": "/ai-teacher",
                        "btn_text": "Enter Classroom →"
                    }
                ]
            else:
                tasks = [
                    {
                        "step": 1,
                        "time_badge": "25 Mins",
                        "title": "Full Section Cambridge CBT Simulation",
                        "desc": "কঠিনতম অ্যাকাডেমিক রিডিং বা লিসেনিং সেকশনের নিখুঁত অফিশিয়াল প্র্যাকটিস।",
                        "url": "/mock-exam",
                        "btn_text": "Start CBT Mock →"
                    },
                    {
                        "step": 2,
                        "time_badge": "25 Mins",
                        "title": "Writing Task 2 Band 9 Cohesion & Nuance",
                        "desc": "উচ্চস্তরের আর্গুমেন্টেশন ও ব্যালেন্সড অ্যাকাডেমিক পার্সপেক্টিভ দিয়ে প্রবন্ধ রচনা।",
                        "url": "/practice?skill=Writing",
                        "btn_text": "Write Essay →"
                    },
                    {
                        "step": 3,
                        "time_badge": "20 Mins",
                        "title": "C2 Advanced Lexicon & Idiomatic Collocations",
                        "desc": "ন্যাচারাল ব্রিটিশ/অ্যাকাডেমিক কোলোকেশন ও সঠিক রেজিস্টার ড্রিল।",
                        "url": "/vocabulary",
                        "btn_text": "Master Vocab →"
                    },
                    {
                        "step": 4,
                        "time_badge": "20 Mins",
                        "title": "Speaking Part 3 Abstract Logic with ARIA",
                        "desc": "এক্সামিনারের সাথে জটিল বিষয় নিয়ে হাই-ব্যান্ড আলোচনা ও প্রনান্সিয়েশন ফাইন-টিউনিং।",
                        "url": "/ai-teacher",
                        "btn_text": "Interview with ARIA →"
                    }
                ]

        return tasks

    @staticmethod
    def generate_individual_master_plan(user_id: int = 1) -> dict:
        """Generates a 100% individual study plan tailored to the student's target band, daily study mins, and prep duration."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ielts_type, target_band, current_level, daily_study_mins, 
                   prep_duration_days, prep_start_date, custom_ai_plan_json 
            FROM profiles WHERE user_id = ?
        """, (user_id,))
        profile = cursor.fetchone()
        
        cursor.execute("""
            SELECT question_type 
            FROM mistake_notebook 
            WHERE user_id = ? 
            ORDER BY id DESC LIMIT 1
        """, (user_id,))
        weakest = cursor.fetchone()

        conn.close()

        import datetime
        today = datetime.date.today()

        target = float(profile["target_band"]) if profile and profile["target_band"] else 7.5
        current_lvl = float(profile["current_level"]) if profile and profile["current_level"] else 0.0
        mins = int(profile["daily_study_mins"]) if profile and profile["daily_study_mins"] else 45
        duration_days = int(profile["prep_duration_days"]) if profile and profile["prep_duration_days"] else 30
        start_date_str = profile["prep_start_date"] if profile and profile["prep_start_date"] else today.isoformat()
        
        try:
            start_date = datetime.date.fromisoformat(start_date_str)
        except Exception:
            start_date = today

        elapsed_days = max(1, (today - start_date).days + 1)
        current_day = min(elapsed_days, duration_days)
        days_remaining = max(0, duration_days - current_day)
        progress_pct = round((current_day / duration_days) * 100, 1)

        # Dynamic Phases partitioned to student's chosen duration
        p1_end = max(1, round(duration_days * 0.25))

        p2_end = max(p1_end + 1, round(duration_days * 0.50))
        p3_end = max(p2_end + 1, round(duration_days * 0.75))
        p4_end = duration_days

        phases = [
            {
                "phase": 1,
                "days_range": f"Days 1–{p1_end}",
                "title": "Foundations & Diagnostics",
                "desc": "১৬টি ব্যাকরণ রুলস, প্রশ্ন ফরম্যাট ও বেসিক কৌশল আয়ত্ত করা।",
                "status": "CURRENT" if current_day <= p1_end else "COMPLETED"
            },
            {
                "phase": 2,
                "days_range": f"Days {p1_end+1}–{p2_end}",
                "title": "Strategy & Trap Elimination",
                "desc": "বিভ্রান্তিকর অপশন, ট্র্যাপস ও দ্রুত প্যারাফ্রেজিং ডিকোড করা।",
                "status": "CURRENT" if p1_end < current_day <= p2_end else ("COMPLETED" if current_day > p2_end else "UPCOMING")
            },
            {
                "phase": 3,
                "days_range": f"Days {p2_end+1}–{p3_end}",
                "title": "Section Mocks & Speed Polish",
                "desc": "টাইমড মক টেস্ট এবং ভুলের কারণ নোটবুকে চুলচেরা বিশ্লেষণ।",
                "status": "CURRENT" if p2_end < current_day <= p3_end else ("COMPLETED" if current_day > p3_end else "UPCOMING")
            },
            {
                "phase": 4,
                "days_range": f"Days {p3_end+1}–{p4_end}",
                "title": f"Cambridge CBT & Band {target} Polish",
                "desc": "ফুল টেস্ট সিমুলেশন ও ফাইনাল ব্যান্ড স্কোর কনফিডেন্স।",
                "status": "CURRENT" if current_day > p3_end else "UPCOMING"
            }
        ]

        # All-Inclusive Skill Coverage Matrix
        all_skills_coverage = [
            {"skill": "Reading", "icon": "📖", "badge": None, "desc": "Question Traps & Fast Skimming", "link": "/practice?skill=Reading"},
            {"skill": "Listening", "icon": "🎧", "badge": None, "desc": "Section 1-4 Form & Audio Traps", "link": "/practice?skill=Listening"},
            {"skill": "Writing", "icon": "✍️", "badge": None, "desc": "Task 1 Trends & Task 2 Essays", "link": "/practice?skill=Writing"},
            {"skill": "Speaking", "icon": "🗣️", "badge": None, "desc": "Part 1-3 Live Socratic Interview", "link": "/ai-teacher"},
            {"skill": "Grammar", "icon": "📝", "badge": None, "desc": "Academic Sentence Mechanics", "link": "/grammar"},
            {"skill": "Vocabulary", "icon": "🔤", "badge": None, "desc": "High-Yield Theme Banks", "link": "/vocabulary"},
            {"skill": "Mock CBT", "icon": "🏆", "badge": "Simulators", "desc": "Full Official Computer Test", "link": "/mock-exam"},
            {"skill": "Mistake Log", "icon": "📒", "badge": "Diagnostics", "desc": "Weakness Notebook Review", "link": "/mistake-notebook"}
        ]

        weak_type = weakest["question_type"] if weakest else None
        tasks = AdaptiveLearningEngine.build_tailored_tasks(target, mins, weak_type)

        if duration_days <= 15:
            prep_title = "⚡ 15-Day Express Sprint"
        elif duration_days <= 30:
            prep_title = "🎯 30-Day Intensive Fast-Track"
        elif duration_days <= 60:
            prep_title = "🚀 60-Day Comprehensive Master"
        else:
            prep_title = "🏆 90-Day Elite Transformation"

        advice = {
            "title": f"🎯 Personalized Strategy for Band {target}",
            "bengali": f"আপনার লক্ষ্য Band {target} অর্জনের জন্য আগামী {days_remaining} দিন অত্যন্ত গুরুত্বপূর্ণ। প্রতিদিন {mins} মিনিটের ফোকাসড সেশনে প্রতিটি স্কিল সমান গুরুত্বের সাথে অনুশীলন করুন।"
        }

        return {
            "target_band": target,
            "current_level": current_lvl,
            "allocated_mins": mins,
            "duration_days": duration_days,
            "current_day": current_day,
            "days_remaining": days_remaining,
            "progress_pct": progress_pct,
            "prep_title": prep_title,
            "phases": phases,
            "all_skills_coverage": all_skills_coverage,
            "today_tasks": tasks,
            "total_steps": len(tasks),
            "advice": advice,
            "recommended_focus": weak_type or ("True / False / Not Given" if target < 8.0 else "Inferences & Summary Completion"),
            "primary_cta": "Start Today's Targeted Practice"
        }

    @staticmethod
    def generate_daily_study_plan(user_id: int = 1) -> dict:
        """Alias that forwards to generate_individual_master_plan."""
        return AdaptiveLearningEngine.generate_individual_master_plan(user_id)
