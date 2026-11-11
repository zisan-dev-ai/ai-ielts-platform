import sqlite3
import json
import os
import time
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "ielts_platform.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30.0)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Student Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        ielts_type TEXT DEFAULT 'Academic',
        target_band REAL DEFAULT 7.5,
        current_level REAL DEFAULT 6.0,
        exam_date TEXT,
        daily_study_mins INTEGER DEFAULT 45,
        prep_duration_days INTEGER DEFAULT 30,
        prep_start_date TEXT,
        custom_ai_plan_json TEXT,
        mother_language TEXT DEFAULT 'Bengali',
        teacher_language_pref TEXT DEFAULT 'English + Mother Language',
        onboarding_completed INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    """)

    # AI Provider & Credentials Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_providers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        is_enabled INTEGER DEFAULT 1,
        priority INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_id TEXT NOT NULL,
        api_key_masked TEXT NOT NULL,
        api_key TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        latency_ms INTEGER DEFAULT 0,
        error_count INTEGER DEFAULT 0,
        last_used_at TIMESTAMP,
        last_tested_at TIMESTAMP,
        label TEXT DEFAULT '',
        FOREIGN KEY (provider_id) REFERENCES ai_providers (id)
    )
    """)

    try:
        cursor.execute("ALTER TABLE ai_credentials ADD COLUMN label TEXT DEFAULT ''")
    except Exception:
        pass

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_request_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_id TEXT NOT NULL,
        task_type TEXT NOT NULL,
        prompt_tokens INTEGER DEFAULT 0,
        completion_tokens INTEGER DEFAULT 0,
        latency_ms INTEGER DEFAULT 0,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Questions & Content Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill TEXT NOT NULL,
        ielts_type TEXT DEFAULT 'Academic',
        test_type TEXT DEFAULT 'Academic',
        section_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        passage_or_context TEXT,
        audio_url TEXT,
        question_type TEXT NOT NULL,
        sub_type_tag TEXT DEFAULT '',
        question_text TEXT NOT NULL,
        options_json TEXT,
        answer_key TEXT NOT NULL,
        explanation TEXT,
        difficulty TEXT DEFAULT 'Medium',
        cambridge_book INTEGER DEFAULT 19,
        test_number INTEGER DEFAULT 1,
        passage_or_section INTEGER DEFAULT 1,
        difficulty_band REAL DEFAULT 7.0,
        group_id TEXT DEFAULT '',
        group_instructions TEXT DEFAULT '',
        trap_type TEXT DEFAULT '',
        synonym_mapping_json TEXT DEFAULT '[]'
    )
    """)

    q_columns = [
        ('test_type', "TEXT DEFAULT 'Academic'"),
        ('ielts_type', "TEXT DEFAULT 'Academic'"),
        ('sub_type_tag', "TEXT DEFAULT ''"),
        ('cambridge_book', "INTEGER DEFAULT 19"),
        ('test_number', "INTEGER DEFAULT 1"),
        ('passage_or_section', "INTEGER DEFAULT 1"),
        ('difficulty_band', "REAL DEFAULT 7.0"),
        ('group_id', "TEXT DEFAULT ''"),
        ('group_instructions', "TEXT DEFAULT ''"),
        ('trap_type', "TEXT DEFAULT ''"),
        ('synonym_mapping_json', "TEXT DEFAULT '[]'"),
        ('audio_url', "TEXT DEFAULT ''")
    ]
    for col, col_def in q_columns:
        try:
            cursor.execute(f"ALTER TABLE questions ADD COLUMN {col} {col_def}")
        except Exception:
            pass

    # Writing Submissions & Evaluations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS writing_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_type TEXT NOT NULL,
        prompt_title TEXT NOT NULL,
        prompt_text TEXT NOT NULL,
        submission_text TEXT NOT NULL,
        word_count INTEGER DEFAULT 0,
        time_spent_seconds INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS writing_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER UNIQUE NOT NULL,
        task_achievement REAL NOT NULL,
        coherence_cohesion REAL NOT NULL,
        lexical_resource REAL NOT NULL,
        grammatical_range REAL NOT NULL,
        overall_band REAL NOT NULL,
        strengths_json TEXT,
        weaknesses_json TEXT,
        line_by_line_errors_json TEXT,
        improvement_plan TEXT,
        provider_used TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (submission_id) REFERENCES writing_submissions (id) ON DELETE CASCADE
    )
    """)

    # Speaking Sessions & Evaluations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS speaking_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        part_number INTEGER NOT NULL,
        prompt_title TEXT NOT NULL,
        prompt_text TEXT NOT NULL,
        audio_file_path TEXT,
        transcript TEXT,
        time_spent_seconds INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS speaking_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER UNIQUE NOT NULL,
        fluency_coherence REAL NOT NULL,
        lexical_resource REAL NOT NULL,
        grammatical_range REAL NOT NULL,
        pronunciation REAL NOT NULL,
        overall_band REAL NOT NULL,
        strengths_json TEXT,
        weaknesses_json TEXT,
        phonetic_feedback_json TEXT,
        improvement_plan TEXT,
        provider_used TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES speaking_sessions (id) ON DELETE CASCADE
    )
    """)

    # Practice Results (Reading & Listening)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        question_id INTEGER NOT NULL,
        user_answer TEXT NOT NULL,
        is_correct INTEGER NOT NULL,
        time_taken_seconds INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Mistake Notebook
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mistake_notebook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        question_type TEXT NOT NULL,
        question_title TEXT NOT NULL,
        user_answer TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT,
        mastery_status TEXT DEFAULT 'Needs Practice',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Adaptive Skill Graph & Mastery
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skill_mastery (
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        question_type TEXT NOT NULL,
        total_attempted INTEGER DEFAULT 0,
        total_correct INTEGER DEFAULT 0,
        independent_correct INTEGER DEFAULT 0,
        assisted_correct INTEGER DEFAULT 0,
        mastery_percentage REAL DEFAULT 0.0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, skill, question_type),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Add independent_correct & assisted_correct columns if missing
    try:
        cursor.execute("ALTER TABLE skill_mastery ADD COLUMN independent_correct INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE skill_mastery ADD COLUMN assisted_correct INTEGER DEFAULT 0")
    except Exception:
        pass

    # Student Personalized Learning Path
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_learning_path (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        topic_key TEXT NOT NULL,
        current_phase TEXT DEFAULT 'teaching',
        mastery_score REAL DEFAULT 0.0,
        unlock_status TEXT DEFAULT 'active',
        order_index INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Comprehensive Student Mistake Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_mistake_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        question_type TEXT NOT NULL,
        student_answer TEXT,
        correct_answer TEXT,
        mistake_category TEXT DEFAULT 'strategy_error',
        hints_needed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Grammar Rules Catalog
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grammar_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level_tier TEXT NOT NULL, -- 'Foundational (Band 5.0-6.0)', 'Intermediate (Band 6.5-7.0)', 'Advanced Master (Band 7.5-9.0)'
        topic_name TEXT NOT NULL,
        rule_description TEXT NOT NULL,
        common_error TEXT NOT NULL,
        correct_example TEXT NOT NULL,
        cambridge_tip TEXT
    )
    """)

    # Vocabulary Catalog (C1/C2 IELTS Academic)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocab_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        cefr_level TEXT DEFAULT 'C1',
        topic_tag TEXT DEFAULT 'Academic General',
        meaning TEXT NOT NULL,
        collocations_json TEXT,
        synonyms_json TEXT,
        example_sentence TEXT NOT NULL
    )
    """)

    # Spaced Repetition System (SRS) & Student Vocab Learning Progress
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocab_user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL DEFAULT 1,
        word TEXT NOT NULL,
        topic_id TEXT NOT NULL,
        mastery_level INTEGER DEFAULT 0, -- 0: New, 1: Learning, 2: Review Due, 3: Mastered
        last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        next_review_due TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        correct_count INTEGER DEFAULT 0,
        mistake_count INTEGER DEFAULT 0,
        user_sentences_json TEXT DEFAULT '[]',
        UNIQUE(user_id, word)
    )
    """)

    # Auto-Detected Grammar & Vocab Error Log from Essays/Speaking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grammar_error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        source_module TEXT NOT NULL, -- 'Writing Task 1', 'Writing Task 2', 'Speaking Part 2'
        error_type TEXT NOT NULL, -- 'Subject-Verb Agreement', 'Articles', 'Preposition', etc.
        flagged_sentence TEXT NOT NULL,
        suggested_correction TEXT NOT NULL,
        explanation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Student Grammar & Vocab Mastery Tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_grammar_vocab_mastery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_type TEXT NOT NULL, -- 'grammar' or 'vocabulary'
        topic_or_word TEXT NOT NULL,
        category TEXT,
        mastery_stage TEXT DEFAULT 'Seen', -- 'Seen', 'Recognized', 'Understood', 'Contextualized', 'Mastered'
        passive_mastery_pct REAL DEFAULT 0.0,
        active_mastery_pct REAL DEFAULT 0.0,
        last_practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Ensure default student user and profile exist
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password_hash) VALUES (1, 'Student', 'student@ielts.ai', 'hashed')")
    cursor.execute("INSERT OR IGNORE INTO profiles (user_id, ielts_type, target_band, current_level) VALUES (1, 'Academic', 7.5, 6.0)")

    # Seed baseline Grammar Rules if empty
    cursor.execute("SELECT COUNT(*) FROM grammar_rules")
    if cursor.fetchone()[0] == 0:
        rules_seed = [
            ("Foundational (Band 5.0-6.0)", "Subject-Verb Agreement", "Singular subjects require singular verbs, plural subjects require plural verbs.", "The list of items are on the desk.", "The list of items is on the desk.", "Watch out for prepositional phrases between subject and verb."),
            ("Foundational (Band 5.0-6.0)", "Articles (A/An/The)", "Use 'the' for specific nouns known to the reader; omit before general uncountable nouns.", "The government should invest in the education.", "The government should invest in education.", "Abstract nouns like education, health, and pollution rarely take 'the' in general statements."),
            ("Intermediate (Band 6.5-7.0)", "Complex Sentence Structures", "Combine an independent clause with one or more dependent clauses using subordinate conjunctions.", "Although it rained. We went outside.", "Although it rained, we went outside.", "Writing Task 2 requires a variety of complex sentences for Band 7.0+ Grammatical Range."),
            ("Intermediate (Band 6.5-7.0)", "Conditionals (Type 2 & 3)", "Use Type 2 for hypothetical present situations and Type 3 for past hypothetical regrets.", "If governments invest more, pollution will decrease.", "If governments were to invest more, pollution would decrease significantly.", "Hypothetical arguments add sophistication to Writing Task 2 body paragraphs."),
            ("Advanced Master (Band 7.5-9.0)", "Inversion for Emphasis", "Invert subject and auxiliary verb after negative adverbial phrases (e.g. Not only, Rarely, Seldom).", "Not only governments should act, but also individuals.", "Not only should governments act, but individuals must also take responsibility.", "Inversion showcases Band 8.5+ advanced grammatical control when used accurately."),
            ("Advanced Master (Band 7.5-9.0)", "Nominalization", "Convert verbs and adjectives into academic noun phrases to create an objective formal tone.", "Because cars increased rapidly, air quality got worse.", "The rapid increase in motor vehicles resulted in severe air quality degradation.", "Nominalization is essential for Band 8.0 Task 1 reports and Task 2 academic tone.")
        ]
        cursor.executemany("INSERT INTO grammar_rules (level_tier, topic_name, rule_description, common_error, correct_example, cambridge_tip) VALUES (?, ?, ?, ?, ?, ?)", rules_seed)

    # Seed baseline student mastery for grammar topics if empty
    cursor.execute("SELECT COUNT(*) FROM student_grammar_vocab_mastery WHERE user_id = 1")
    if cursor.fetchone()[0] == 0:
        mastery_seed = [
            (1, 'grammar', 'Subject-Verb Agreement', 'Foundational (Band 5.0-6.0)', 'Recognized', 85.0, 60.0),
            (1, 'grammar', 'Articles (A/An/The)', 'Foundational (Band 5.0-6.0)', 'Understood', 70.0, 45.0),
            (1, 'grammar', 'Complex Sentence Structures', 'Intermediate (Band 6.5-7.0)', 'Contextualized', 65.0, 50.0),
            (1, 'grammar', 'Conditionals (Type 2 & 3)', 'Intermediate (Band 6.5-7.0)', 'Seen', 55.0, 40.0),
            (1, 'grammar', 'Inversion for Emphasis', 'Advanced Master (Band 7.5-9.0)', 'Seen', 35.0, 20.0),
            (1, 'grammar', 'Nominalization', 'Advanced Master (Band 7.5-9.0)', 'Seen', 40.0, 25.0)
        ]
        cursor.executemany("INSERT INTO student_grammar_vocab_mastery (user_id, item_type, topic_or_word, category, mastery_stage, passive_mastery_pct, active_mastery_pct) VALUES (?, ?, ?, ?, ?, ?, ?)", mastery_seed)

    # Seed initial auto-detected error logs if empty
    cursor.execute("SELECT COUNT(*) FROM grammar_error_logs")
    if cursor.fetchone()[0] == 0:
        error_seed = [
            (1, "Writing Task 2", "Subject-Verb Agreement", "The number of students which is attending the course have increased.", "The number of students attending the course has increased.", "When 'the number of' is the subject, use a singular verb ('has')."),
            (1, "Speaking Part 2", "Articles (A/An/The)", "I lived in UK for three years to study environmental science.", "I lived in the UK for three years to study environmental science.", "Country names containing 'United' require the definite article 'the'.")
        ]
        cursor.executemany("INSERT INTO grammar_error_logs (user_id, source_module, error_type, flagged_sentence, suggested_correction, explanation) VALUES (?, ?, ?, ?, ?, ?)", error_seed)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
