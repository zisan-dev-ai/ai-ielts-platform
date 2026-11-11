import json
from ai_engine.ai_router import AIRouter

router = AIRouter()
words = [
    'Tertiary education',
    'Cognitive development',
    'Holistic pedagogical approach',
    'Curricular reform',
    'Standardized assessment'
]

prompt = "For each of the following IELTS Academic terms, provide 2 to 4 high-quality academic synonyms (or paraphrases) and 1 to 3 antonyms (or contrasting concepts). Return strictly a JSON dictionary where keys are the exact terms, and values are objects with 'synonyms' (list of strings) and 'antonyms' (list of strings).\n\nTerms:\n" + "\n".join(f"- {w}" for w in words)

res = router.generate_json(prompt, system_instruction="You are an expert IELTS Academic Lexicographer. Return strictly JSON.")
print(json.dumps(res, indent=2))
