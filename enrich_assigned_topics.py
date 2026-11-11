# -*- coding: utf-8 -*-
"""
Enrichment script for:
- language
- media
- tourism
- transport
Updates vocab_db JSON files and verifies 0 generic fallbacks remain.
"""
import os
import sys
import json

PLATFORM_DIR = os.path.dirname(os.path.abspath(__file__))
VOCAB_DIR = os.path.join(PLATFORM_DIR, "ai_engine", "vocab_db")

# Import the four lexicons from project directory
if PLATFORM_DIR not in sys.path:
    sys.path.insert(0, PLATFORM_DIR)

from lexicon_language import LEXICON_LANGUAGE
from lexicon_media import LEXICON_MEDIA
from lexicon_tourism import LEXICON_TOURISM
from lexicon_transport import LEXICON_TRANSPORT

TOPIC_LEXICONS = {
    "language": LEXICON_LANGUAGE,
    "media": LEXICON_MEDIA,
    "tourism": LEXICON_TOURISM,
    "transport": LEXICON_TRANSPORT
}

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

def needs_fix(word_obj):
    w = word_obj.get("word", "")
    syns = word_obj.get("synonyms", [])
    ants = word_obj.get("antonyms", [])
    return is_generic_syn(syns, w) or is_generic_ant(ants)

def run():
    print("=" * 60)
    print("STARTING LEXICAL ENRICHMENT FOR ASSIGNED TOPICS")
    print("=" * 60)

    total_updated = 0
    topic_results = {}

    for topic_id, lexicon in TOPIC_LEXICONS.items():
        fpath = os.path.join(VOCAB_DIR, f"{topic_id}.json")
        if not os.path.exists(fpath):
            print(f"Error: File not found: {fpath}")
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        words = data.get("words", [])
        updated_count = 0

        # Update words
        for w in words:
            name = w.get("word")
            if name in lexicon:
                w["synonyms"] = lexicon[name]["synonyms"]
                w["antonyms"] = lexicon[name]["antonyms"]
                updated_count += 1
                total_updated += 1

        # Atomic write back
        tmp_path = fpath + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, fpath)

        # Verification pass
        with open(fpath, "r", encoding="utf-8") as f:
            verified_data = json.load(f)
        
        remaining_fix = [w["word"] for w in verified_data.get("words", []) if needs_fix(w)]
        topic_results[topic_id] = {
            "total_words": len(words),
            "enriched_words": updated_count,
            "remaining_generic": len(remaining_fix),
            "remaining_list": remaining_fix
        }

        print(f"[{topic_id:10}] Enriched: {updated_count:3d} / {len(words):3d} words | Generic Remaining: {len(remaining_fix)}")
        if remaining_fix:
            print(f"  FAILED WORDS in {topic_id}: {remaining_fix}")

    print("=" * 60)
    print(f"TOTAL WORDS ENRICHED: {total_updated}")
    all_zero = all(r["remaining_generic"] == 0 for r in topic_results.values())
    if all_zero:
        print("VERIFICATION PASSED: ALL 4 TOPICS HAVE 0 GENERIC FALLBACKS REMAINING!")
    else:
        print("VERIFICATION FAILED: Some words still have generic fallbacks!")
    print("=" * 60)

    # Output JSON summary to stdout
    print("\nSUMMARY_JSON:" + json.dumps(topic_results))

if __name__ == "__main__":
    run()
