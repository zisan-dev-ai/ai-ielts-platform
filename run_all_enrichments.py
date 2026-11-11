# -*- coding: utf-8 -*-
"""
Orchestrator to enrich environment, health, and technology vocabularies
and verify 0 generic fallbacks remain.
"""
import os
import sys
import json

PLATFORM_DIR = os.path.dirname(os.path.abspath(__file__))
if PLATFORM_DIR not in sys.path:
    sys.path.insert(0, PLATFORM_DIR)

from enrich_env import update_environment, ENV_LEXICON
from enrich_health import update_health, HEALTH_LEXICON
from enrich_tech import update_technology, TECH_LEXICON

GENERIC_SYN_PREFIXES = [
    "Systemic ", "Formal ", "Authentic ", "To ", "Perform ", "Distinctly ",
    "Highly ", "In a ", "With ", "Of "
]
GENERIC_ANT_VALUES = [
    "Absence of the condition", "Contrasting state",
    "Neglect to act", "Abstain from action",
    "Zero occurrence", "Absolute zero",
    "Dismissal of charges", "Unconditional release"
]

def is_generic_syn(syns, word):
    if not syns or len(syns) == 0:
        return True
    for s in syns:
        for pfx in GENERIC_SYN_PREFIXES:
            if s.startswith(pfx) and (word.lower() in s.lower() or len(s.split()) > 4):
                return True
    for s in syns:
        if s.strip().lower() == word.strip().lower():
            return True
    return False

def is_generic_ant(ants):
    if not ants or len(ants) == 0:
        return True
    for a in ants:
        if a in GENERIC_ANT_VALUES:
            return True
    return False

def verify_topic(topic_id):
    path = os.path.join(PLATFORM_DIR, "ai_engine", "vocab_db", f"{topic_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    words = data.get("words", [])
    generic_words = []
    for w in words:
        name = w.get("word", "")
        syns = w.get("synonyms", [])
        ants = w.get("antonyms", [])
        if is_generic_syn(syns, name) or is_generic_ant(ants):
            generic_words.append((name, syns, ants))
    return len(words), generic_words

def main():
    print("=== STARTING ENRICHMENT ===")
    env_count = update_environment()
    health_count = update_health()
    tech_count = update_technology()
    
    print("\n=== VERIFYING RESULTS ===")
    all_clean = True
    for topic in ["environment", "health", "technology"]:
        total, bad = verify_topic(topic)
        print(f"Topic '{topic}': Total words = {total}, Generic remaining = {len(bad)}")
        if bad:
            all_clean = False
            for b in bad[:5]:
                print(f"  [BAD] {b[0]}: syns={b[1]}, ants={b[2]}")
    
    if all_clean:
        print("\nALL 3 TOPICS VERIFIED: 0 generic fallbacks remaining!")
    else:
        print("\nWARNING: Some generic fallbacks remain.")
        sys.exit(1)

if __name__ == "__main__":
    main()
