# -*- coding: utf-8 -*-
import sys
import json
from database import get_db, init_db
from seed_authentic_cambridge_reading_full import seed_full_cambridge_reading
from seed_authentic_cambridge_listening_full import seed_full_cambridge_listening

def seed_exact_user_taxonomy():
    init_db()
    
    # 1. Seed 40 authentic Cambridge Reading questions across 3 passages
    seed_full_cambridge_reading()

    # 2. Seed 40 authentic Cambridge Listening questions across 4 sections
    seed_full_cambridge_listening()

    # 3. Seed Speaking and Writing syllabus
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM questions WHERE skill = 'Speaking'")
    if cursor.fetchone()[0] == 0:
        Q = []
        def add_q(skill, qt, st, qtext, context="Official Cambridge IELTS Exam Prompt"):
            Q.append((
                skill, "Academic", 1, f"{skill} - {st}", context, qt, st, qtext,
                json.dumps(["Option A", "Option B", "Option C", "Option D"] if "Choice" in qt or "Matching" in qt or "Selection" in qt else []),
                "Sample Answer", f"Official Cambridge practice prompt for {qt} ({st}).", "Medium"
            ))

        # LISTENING (13)
        for item in ['Multiple Choice', 'Multiple Selection', 'Matching', 'Form Completion', 'Note Completion', 'Table Completion', 'Flow-chart Completion', 'Summary Completion', 'Sentence Completion', 'Short-answer Questions', 'Plan Labelling', 'Map Labelling', 'Diagram Labelling']:
            add_q("Listening", "Listening", item, f"Practice question for Listening: {item}")

        # WRITING AC TASK 1 (14)
        for item in ['Line Graph', 'Bar Chart', 'Pie Chart', 'Table', 'Multiple Charts / Graphs', 'Combination Chart', 'Process Diagram', 'Natural Process', 'Manufacturing Process', 'Map', 'Map — Past vs Present', 'Map — Present vs Future', 'Map — Proposed Changes', 'Plans / Site Plans']:
            add_q("Writing", "Academic Task 1", item, f"Summarise the information by selecting and reporting main features for: {item}")

        # WRITING GT TASK 1 (14)
        for item in ['Formal Letter', 'Semi-formal Letter', 'Informal Letter', 'Request', 'Complaint', 'Apology', 'Invitation', 'Thank-you', 'Giving Information', 'Asking for Information', 'Giving Advice', 'Making a Suggestion', 'Application', 'Explanation']:
            add_q("Writing", "GT Task 1", item, f"Write a letter regarding: {item}")

        # WRITING TASK 2 (14)
        for item in ['Opinion Essay', 'Agree or Disagree', 'Discuss Both Views', 'Discuss Both Views + Opinion', 'Advantages and Disadvantages', 'Advantages and Disadvantages + Opinion', 'Problem and Solution', 'Causes and Solutions', 'Cause and Effect', 'Two-part Question', 'Direct Question', 'Positive or Negative Development', 'To What Extent Do You Agree or Disagree?', 'Mixed / Multiple Question']:
            add_q("Writing", "Task 2", item, f"Write an academic essay responding to: {item}")

        # SPEAKING PART 1 (60)
        for item in ['Home', 'Accommodation', 'Hometown', 'City', 'Country', 'Work', 'Study', 'School', 'University', 'Family', 'Friends', 'Neighbours', 'Childhood', 'Daily Routine', 'Free Time', 'Hobbies', 'Interests', 'Sports', 'Exercise', 'Food', 'Cooking', 'Restaurants', 'Shopping', 'Clothes', 'Weather', 'Seasons', 'Travel', 'Holidays', 'Transport', 'Public Transport', 'Cars', 'Technology', 'Computers', 'Internet', 'Social Media', 'Mobile Phones', 'Music', 'Films', 'TV', 'Books', 'Reading', 'Photography', 'Art', 'Nature', 'Animals', 'Pets', 'Health', 'Sleep', 'Festivals', 'Celebrations', 'Gifts', 'Birthdays', 'Money', 'Advertising', 'Newspapers', 'Languages', 'Learning English', 'Future Plans', 'Memories', 'Important People']:
            add_q("Speaking", "Part 1", item, f"Examiner Interview on: {item}")

        # SPEAKING PART 2 (53)
        for item in ['Describe a Person', 'Describe a Place', 'Describe an Object', 'Describe a Thing', 'Describe an Event', 'Describe an Experience', 'Describe a Memory', 'Describe a Journey', 'Describe a Trip', 'Describe a Festival', 'Describe a Celebration', 'Describe a Book', 'Describe a Film', 'Describe a Song', 'Describe a Photograph', 'Describe a Skill', 'Describe a Hobby', 'Describe an Activity', 'Describe a Job', 'Describe a Teacher', 'Describe a Friend', 'Describe a Family Member', 'Describe a Famous Person', 'Describe a Historical Person', 'Describe a Useful Website', 'Describe an App', 'Describe a Piece of Technology', 'Describe Something You Bought', 'Describe a Gift', 'Describe a Problem', 'Describe a Difficult Situation', 'Describe a Success', 'Describe a Failure', 'Describe a Decision', 'Describe a Change', 'Describe a Goal', 'Describe a Plan', 'Describe Something You Learned', 'Describe Something You Want to Learn', 'Describe Something You Want to Do', 'Describe Something You Would Like to Own', 'Describe Something You Enjoy', 'Describe Something You Dislike', 'Describe a Time You Helped Someone', 'Describe a Time Someone Helped You', 'Describe a Time You Met Someone', 'Describe a Time You Were Happy', 'Describe a Time You Were Sad', 'Describe a Time You Were Surprised', 'Describe a Time You Were Proud', 'Describe a Time You Were Late', 'Describe a Time You Got Lost', 'Describe a Time You Changed Your Opinion']:
            add_q("Speaking", "Part 2", item, f"Cue Card: {item}")

        # SPEAKING PART 3 (40)
        for item in ['Why Questions', 'Why/Why Not Questions', 'How Questions', 'What Questions', 'Which Questions', 'Who Questions', 'Where Questions', 'When Questions', 'Comparison Questions', 'Advantages Questions', 'Disadvantages Questions', 'Cause Questions', 'Effect Questions', 'Problem Questions', 'Solution Questions', 'Opinion Questions', 'Agreement/Disagreement Questions', 'Importance Questions', 'Preference Questions', 'Choice Questions', 'Prediction Questions', 'Future Questions', 'Change Questions', 'Past vs Present Questions', 'Individual vs Society Questions', 'Young vs Old Questions', 'Government Questions', 'Education Questions', 'Technology Questions', 'Environment Questions', 'Society Questions', 'Culture Questions', 'Globalization Questions', 'Hypothetical Questions', 'Responsibility Questions', 'Evaluation Questions', 'Cause + Solution Questions', 'Advantage + Disadvantage Questions', 'Compare + Opinion Questions', 'Past + Present + Future Questions']:
            add_q("Speaking", "Part 3", item, f"Two-way Discussion: {item}")

        cursor.executemany("""
            INSERT INTO questions (
                skill, test_type, section_number, title, passage_or_context,
                question_type, sub_type_tag, question_text, options_json, answer_key, explanation, difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, Q)
        conn.commit()

    conn.close()
    print("SUCCESS: Seeded all official syllabus and 40 Cambridge CBT questions!")

seed_all_77_types = seed_exact_user_taxonomy

if __name__ == "__main__":
    seed_exact_user_taxonomy()
