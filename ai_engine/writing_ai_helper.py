"""
ARIA AI Writing Co-Pilot & Scaffolding Helper
Provides on-demand Brainstorming, Outlining, Band 8+ Vocabulary,
Paraphrasing, Sentence Polishing, and Interactive Tutor Chat for Cambridge IELTS Writing.
"""

import os
import json
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from ai_engine.gemini_adapter import GeminiAdapter

logger = logging.getLogger(__name__)


def _get_gemini_keys() -> List[str]:
    """Load all active Gemini API keys from DB + environment."""
    keys = []
    try:
        conn = sqlite3.connect("ielts_platform.db")
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT api_key FROM ai_credentials WHERE provider_id='gemini' AND status='Active' ORDER BY id ASC"
        ).fetchall()
        conn.close()
        keys = [r["api_key"] for r in rows if r["api_key"]]
    except Exception:
        pass
    env_k = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_k and env_k not in keys:
        keys.append(env_k)
    return keys


class WritingAIHelper:
    def __init__(self):
        self.gemini = GeminiAdapter()
        self._keys = _get_gemini_keys()

    def _call(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.4) -> str:
        """Universal AI call via AIRouter across any provider (OpenAI, Claude, DeepSeek, Grok, Custom, Gemini)."""
        try:
            from ai_engine.ai_router import ai_router
            return ai_router.generate_text(prompt)
        except Exception:
            pass

        key = self._keys[0] if self._keys else ""
        return self.gemini.generate_text(
            prompt,
            api_key=key,
            api_key_pool=self._keys,
            maxOutputTokens=max_tokens,
            temperature=temperature,
        )

    # ── 1. BRAINSTORM ─────────────────────────────────────────────────────────

    def get_brainstorm_ideas(self, task_type: str, prompt_title: str, prompt_statement: str) -> Dict[str, Any]:
        """Generate rich, task-specific brainstorming ideas."""
        is_t1 = "1" in task_type

        if is_t1:
            role_context = (
                "You are a Cambridge IELTS Band 9 Senior Examiner specialising in Task 1 Academic data interpretation. "
                "The student needs to write a 150-word factual overview of a visual chart/graph/diagram."
            )
            group_a_label = "📊 Key Trends / Patterns to Highlight (rising, dominant, notable)"
            group_b_label = "📉 Secondary Patterns & Contrasts (declining, fluctuating, exceptions)"
            extra_keys = '"ov_sentence_1": "First overview sentence highlighting single most dominant trend", "ov_sentence_2": "Second overview sentence contrasting or noting another major trend",'
        else:
            role_context = (
                "You are a Cambridge IELTS Band 9 Senior Examiner and Trainer specialising in Task 2 academic essays. "
                "The student must write a 250-word balanced, well-argued essay."
            )
            group_a_label = "✅ Arguments SUPPORTING / FOR the proposition (with Band 8 example)"
            group_b_label = "⚠️ Arguments AGAINST / Counterarguments (with Band 8 example)"
            extra_keys = '"band_9_thesis": "A single powerful thesis sentence for the introduction",'

        prompt = f"""{role_context}

Generate structured, exam-quality brainstorming content for this writing task.

Task Type: {task_type}
Topic: {prompt_title}
Full Prompt:
\"\"\"{prompt_statement}\"\"\"

INSTRUCTIONS:
- Each "point" must be a complete, intelligent argument (20-35 words), not a vague heading.
- Each "example" must be a specific, real-world or data-based illustration — NOT generic.
- The examiner_tip must mention a specific IELTS Band Descriptor criterion by name.
- Use academic English throughout.

Respond ONLY in valid JSON, no markdown fences, no extra commentary:
{{
  "main_theme": "One precise sentence summarising the core debate or data topic",
  {extra_keys}
  "key_points_group_a": [
    {{"label": "{group_a_label}", "point": "Detailed argument sentence here.", "example": "Specific real-world example with data or named case study.", "band_phrase": "An academic collocation or Band 8+ phrase to use here"}},
    {{"label": "{group_a_label}", "point": "Detailed argument sentence here.", "example": "Specific real-world example with data or named case study.", "band_phrase": "An academic collocation or Band 8+ phrase to use here"}},
    {{"label": "{group_a_label}", "point": "Detailed argument sentence here.", "example": "Specific real-world example with data or named case study.", "band_phrase": "An academic collocation or Band 8+ phrase to use here"}}
  ],
  "key_points_group_b": [
    {{"label": "{group_b_label}", "point": "Detailed counter-argument sentence here.", "example": "Specific real-world example with data or named case study.", "band_phrase": "An academic collocation or Band 8+ phrase to use here"}},
    {{"label": "{group_b_label}", "point": "Detailed counter-argument sentence here.", "example": "Specific real-world example with data or named case study.", "band_phrase": "An academic collocation or Band 8+ phrase to use here"}}
  ],
  "examiner_tip": "Specific Band Descriptor advice with the criterion name (e.g. Task Achievement, Coherence & Cohesion, Lexical Resource, GRA) and a concrete strategy."
}}"""

        try:
            raw = self._call(prompt, max_tokens=2200, temperature=0.4)
            data = self._parse_json(raw)
            if data and "key_points_group_a" in data:
                return data
        except Exception as e:
            logger.error(f"Brainstorm AI error: {e}")

        # Smart fallback
        if is_t1:
            return {
                "main_theme": f"The visual data illustrates key comparative trends related to {prompt_title}.",
                "ov_sentence_1": "Overall, the most striking feature is the dominant upward trajectory of the leading category throughout the entire period.",
                "ov_sentence_2": "By contrast, the remaining categories experienced either stagnation or a marked decline, particularly towards the end of the period shown.",
                "key_points_group_a": [
                    {"label": "📊 Key Trend 1", "point": "Identify and describe the single highest-performing category using precise figures from the start and end of the period.", "example": "e.g., Category X rose sharply from 12% in 2000 to a peak of 58% by 2020, more than quadrupling over two decades.", "band_phrase": "witnessed a dramatic surge"},
                    {"label": "📊 Key Trend 2", "point": "Highlight any significant crossover point where two categories exchanged positions — a key feature examiners reward.", "example": "e.g., Category A overtook Category B around 2010, after which the gap widened consistently.", "band_phrase": "experienced a crossover / surpassed"},
                    {"label": "📊 Key Trend 3", "point": "Note any category that remained relatively stable — a detail that shows thorough reading of all data.", "example": "e.g., Category C remained broadly stable throughout, fluctuating marginally between 18% and 22%.", "band_phrase": "remained broadly stable / showed negligible change"}
                ],
                "key_points_group_b": [
                    {"label": "📉 Contrast 1", "point": "Describe the lowest or most sharply declining category using start/end comparison.", "example": "e.g., Category D plummeted from 40% to just 8%, losing the largest proportion of any category.", "band_phrase": "plummeted / experienced a precipitous decline"},
                    {"label": "📉 Contrast 2", "point": "Mention any exceptional fluctuation or anomaly that breaks the general pattern.", "example": "e.g., Despite an initial dip in 2005, Category E staged a modest recovery, ending at 25%.", "band_phrase": "staged a modest recovery / exhibited notable fluctuation"}
                ],
                "examiner_tip": "Task Achievement (Band 8): Your Overview is the most critical paragraph. Do NOT use specific figures there — just state the 2 most dominant overall trends. Save all specific data comparison for Body paragraphs."
            }
        else:
            return {
                "main_theme": f"This prompt debates the socio-economic and ethical implications of {prompt_title}.",
                "band_9_thesis": "While proponents emphasise the long-term benefits for productivity and innovation, critics contend that the associated risks to equity and employment demand comprehensive policy intervention.",
                "key_points_group_a": [
                    {"label": "✅ Argument FOR", "point": "Accelerates socio-economic productivity by automating repetitive tasks, freeing human capital for higher-order cognitive work requiring creativity and critical analysis.", "example": "A 2023 McKinsey Global Institute report found that AI-driven automation increased workforce productivity by 37% in sectors such as financial services and logistics.", "band_phrase": "catalyse unprecedented productivity gains"},
                    {"label": "✅ Argument FOR", "point": "Democratises access to expert-level services — particularly in education and healthcare — reducing systemic inequities between affluent and disadvantaged communities.", "example": "AI diagnostic tools deployed in rural Sub-Saharan Africa have achieved disease detection accuracy comparable to specialist physicians, serving populations with no prior access to specialists.", "band_phrase": "bridge the socio-economic divide / democratise access"},
                    {"label": "✅ Argument FOR", "point": "Stimulates entire new industries and occupational categories, historically generating net employment growth beyond any displacement in the transition period.", "example": "The internet — once feared as a job-destroyer — ultimately created over 3.1 million new roles in e-commerce, digital marketing, and cybersecurity globally by 2010.", "band_phrase": "generate net employment growth in the long run"}
                ],
                "key_points_group_b": [
                    {"label": "⚠️ Counterargument", "point": "Creates structural unemployment for low-skilled and semi-skilled workers who lack the resources or opportunity to reskill rapidly enough to remain competitive in transformed labour markets.", "example": "Oxford Economics projects that up to 20 million manufacturing jobs globally could be displaced by robotics by 2030, disproportionately affecting workers in developing economies.", "band_phrase": "exacerbate structural unemployment / marginalise vulnerable demographics"},
                    {"label": "⚠️ Counterargument", "point": "Concentration of transformative economic benefits within a small technological elite risks deepening wealth inequality and undermining the social contract between citizens and institutions.", "example": "In the United States, the top 1% of tech-sector earners captured over 85% of productivity gains from automation between 2010 and 2022 (Economic Policy Institute, 2023).", "band_phrase": "concentrate economic dividends within a privileged stratum"}
                ],
                "examiner_tip": "Task Achievement (Band 8): Avoid generic arguments like 'it has pros and cons'. Every point MUST be followed by a specific, named example (statistic, institution, country, report). This directly demonstrates the 'fully developed' criterion examiners look for."
            }

    # ── 2. OUTLINE ────────────────────────────────────────────────────────────

    def get_essay_outline(self, task_type: str, prompt_title: str, prompt_statement: str) -> Dict[str, Any]:
        """Generate a complete, exam-ready 4-paragraph blueprint."""
        is_t1 = "1" in task_type
        prompt = f"""You are a Cambridge IELTS Band 9 Writing Trainer. Create a precise, exam-ready 4-paragraph blueprint for this task.

Task Type: {task_type}
Topic: {prompt_title}
Prompt: \"\"\"{prompt_statement}\"\"\"

RULES:
- All example sentences must be fully written out, not placeholder labels.
- The topic sentence of each body paragraph must be a complete, Band 8 sentence.
- Conclusion must NOT introduce new information — only synthesise.

Respond ONLY in valid JSON:
{{
  "paragraph_1_intro": {{
    "goal": "One-line goal of this paragraph",
    "sentence_1": "Fully written paraphrase of the prompt (never copy keywords — use synonyms and grammatical transformation)",
    "sentence_2": "Fully written thesis/overview statement"
  }},
  "paragraph_2_body1": {{
    "goal": "One-line goal",
    "topic_sentence": "Fully written Band 8+ topic sentence",
    "supporting_elaboration": "Fully written 1-2 sentence explanation of WHY this point is valid",
    "illustrative_example": "Fully written specific example with data, institution, or case study"
  }},
  "paragraph_3_body2": {{
    "goal": "One-line goal",
    "topic_sentence": "Fully written Band 8+ topic sentence",
    "supporting_elaboration": "Fully written 1-2 sentence explanation",
    "illustrative_example": "Fully written specific example"
  }},
  "paragraph_4_conclusion": {{
    "goal": "One-line goal",
    "closing_strategy": "Fully written 2-sentence conclusion: restate thesis + final evaluative judgement"
  }}
}}"""

        try:
            raw = self._call(prompt, max_tokens=2200, temperature=0.3)
            data = self._parse_json(raw)
            if data and "paragraph_1_intro" in data:
                return data
        except Exception as e:
            logger.error(f"Outline AI error: {e}")

        if is_t1:
            return {
                "paragraph_1_intro": {"goal": "Paraphrase the visual and state 2 overall trends", "sentence_1": "The provided chart illustrates the comparative figures for the specified categories across the given time period.", "sentence_2": "Overall, it is evident that [leading category] dominated throughout, whereas [declining category] experienced the most pronounced downward trajectory."},
                "paragraph_2_body1": {"goal": "Describe dominant/rising categories with precise data", "topic_sentence": "With regard to the most prominent upward trends, [Category A] recorded the most significant increase, climbing from [X%] in [year] to a peak of [Y%] by [year].", "supporting_elaboration": "This upward trajectory was mirrored, albeit less dramatically, by [Category B], which also rose steadily throughout the period.", "illustrative_example": "Notably, both categories converged around [midpoint], before [A] pulled decisively ahead, ending the period [Z] percentage points above [B]."},
                "paragraph_3_body2": {"goal": "Describe declining/contrasting categories", "topic_sentence": "In stark contrast, [Category C] experienced the sharpest deterioration, plummeting from [X%] to just [Y%] over the same period.", "supporting_elaboration": "Meanwhile, [Category D] remained broadly stable, fluctuating only marginally between [X%] and [Y%], suggesting a relative equilibrium in that sector.", "illustrative_example": "By [final year], the gap between the highest and lowest categories had widened considerably, amounting to a differential of [Z] percentage points."},
                "paragraph_4_conclusion": {"goal": "Note: Task 1 uses an Overview in Para 1 — not a separate conclusion.", "closing_strategy": "Ensure all key trends were captured with accurate units and all figures reference the data accurately without speculation."}
            }
        else:
            return {
                "paragraph_1_intro": {"goal": "Hook, paraphrase, and state clear thesis position", "sentence_1": "The rapid proliferation of [topic-related phenomenon] has generated considerable debate regarding its long-term implications for [society/economy/environment].", "sentence_2": "This essay argues that, while legitimate concerns persist, the cumulative benefits ultimately outweigh the drawbacks, provided that appropriate regulatory safeguards are established."},
                "paragraph_2_body1": {"goal": "First main argument: Benefits with specific evidence", "topic_sentence": "To begin with, the most compelling case in favour of [topic] rests upon its capacity to enhance socio-economic efficiency and stimulate innovation across multiple sectors.", "supporting_elaboration": "When implemented strategically, such advancements enable institutions to redirect human and financial resources towards higher-order challenges that require nuanced judgement and creativity.", "illustrative_example": "A pertinent illustration is the deployment of AI diagnostic systems in NHS hospitals across the UK, which reduced average diagnostic error rates by 27% between 2020 and 2023, according to a peer-reviewed study in The Lancet."},
                "paragraph_3_body2": {"goal": "Counterargument: Risks with evidence, then refutation", "topic_sentence": "On the other hand, critics rightly draw attention to the potential for exacerbating social inequality, as the benefits of such developments tend to accrue disproportionately to technologically privileged demographics.", "supporting_elaboration": "Without deliberate policy intervention — such as progressive taxation on automation profits and subsidised reskilling programmes — a growing segment of the workforce risks permanent marginalisation.", "illustrative_example": "This concern is substantiated by findings from the International Labour Organization (2022), which projected that 14% of existing jobs in OECD nations face a high probability of automation within the next decade, with low-income workers bearing the greatest burden of displacement."},
                "paragraph_4_conclusion": {"goal": "Synthesise and deliver final evaluative judgement", "closing_strategy": "In conclusion, while the risks of entrenched inequality and structural unemployment demand serious policy consideration, the transformative potential of [topic] — when governed by robust ethical frameworks — presents a net positive for modern societies. It is therefore incumbent upon governments and institutions to act proactively rather than reactively in shaping this transition."}
            }

    # ── 3. VOCABULARY ─────────────────────────────────────────────────────────

    def get_topic_vocabulary(self, task_type: str, prompt_title: str, prompt_statement: str) -> Dict[str, Any]:
        """Generate a rich, topic-specific lexical resource vault."""
        prompt = f"""You are an IELTS Lexical Resource Specialist (Band 9). Generate a premium vocabulary vault for this specific IELTS task.

Task: {task_type} — {prompt_title}
Prompt excerpt: {prompt_statement[:300]}

CRITICAL RULES:
- All collocations and phrases must be SPECIFIC to this topic — no generic filler words.
- Each meaning_bn (Bengali) must be accurate, natural Bengali.
- Each example_sentence must use the phrase naturally in academic context.
- Synonyms must be genuinely advanced (Band 8+) — avoid basic alternatives.

Respond ONLY in valid JSON:
{{
  "topic_collocations": [
    {{"phrase": "topic-specific collocation 1", "meaning_bn": "বাংলা অর্থ", "example_sentence": "Full academic example sentence using this phrase.", "band_level": "Band 8"}},
    {{"phrase": "topic-specific collocation 2", "meaning_bn": "বাংলা অর্থ", "example_sentence": "Full academic example sentence.", "band_level": "Band 8"}},
    {{"phrase": "topic-specific collocation 3", "meaning_bn": "বাংলা অর্থ", "example_sentence": "Full academic example sentence.", "band_level": "Band 8.5"}},
    {{"phrase": "topic-specific collocation 4", "meaning_bn": "বাংলা অর্থ", "example_sentence": "Full academic example sentence.", "band_level": "Band 9"}},
    {{"phrase": "topic-specific collocation 5", "meaning_bn": "বাংলা অর্থ", "example_sentence": "Full academic example sentence.", "band_level": "Band 9"}}
  ],
  "academic_synonyms": [
    {{"basic": "increase", "advanced": "surge / escalate / proliferate / witness exponential growth", "context": "When describing data trends or societal changes"}},
    {{"basic": "decrease", "advanced": "plummet / dwindle / undergo a precipitous decline / contract sharply", "context": "Describing downward trends in data or social indicators"}},
    {{"basic": "important", "advanced": "paramount / indispensable / quintessential / of profound consequence", "context": "Evaluating significance in an academic argument"}},
    {{"basic": "problem", "advanced": "predicament / impediment / systemic challenge / pressing dilemma", "context": "Naming issues in Task 2 arguments"}},
    {{"basic": "show", "advanced": "illustrate / underscore / shed light on / attest to / corroborate", "context": "Referring to data or evidence in academic writing"}}
  ],
  "cohesive_devices": [
    {{"category": "Introducing an argument", "phrases": ["To begin with, it is noteworthy that", "Central to this discussion is", "A particularly salient point concerns"]}},
    {{"category": "Adding a supporting point", "phrases": ["Furthermore, it is equally imperative to recognise that", "Compounding this observation is the fact that", "Moreover, empirical evidence corroborates the view that"]}},
    {{"category": "Introducing contrast / counterargument", "phrases": ["In stark contrast to this perspective", "Notwithstanding the aforementioned benefits", "Critics, however, contend that"]}},
    {{"category": "Concluding and synthesising", "phrases": ["Taking all factors into consideration, it is reasonable to deduce that", "In the final analysis, the weight of evidence suggests that", "It therefore follows that"]}},
    {{"category": "Giving examples", "phrases": ["A pertinent illustration of this is", "This is vividly exemplified by", "Empirical evidence for this can be found in"]}}
  ]
}}"""

        try:
            raw = self._call(prompt, max_tokens=2500, temperature=0.3)
            data = self._parse_json(raw)
            if data and "topic_collocations" in data:
                return data
        except Exception as e:
            logger.error(f"Vocabulary AI error: {e}")

        return {
            "topic_collocations": [
                {"phrase": "socio-economic ramifications", "meaning_bn": "সামাজিক ও অর্থনৈতিক পরিণতি বা প্রভাব", "example_sentence": "Policymakers must carefully assess the far-reaching socio-economic ramifications of large-scale automation before endorsing wholesale adoption.", "band_level": "Band 8"},
                {"phrase": "indispensable catalyst for change", "meaning_bn": "পরিবর্তনের অপরিহার্য চালিকাশক্তি", "example_sentence": "Access to quality education has long been regarded as an indispensable catalyst for sustainable socio-economic development.", "band_level": "Band 8.5"},
                {"phrase": "unprecedented exponential surge", "meaning_bn": "নজিরবিহীন দ্রুত ও বিশাল বৃদ্ধি", "example_sentence": "The past decade has witnessed an unprecedented exponential surge in renewable energy adoption across both developed and emerging economies.", "band_level": "Band 9"},
                {"phrase": "systemic structural inequality", "meaning_bn": "কাঠামোগত ব্যবস্থাগত বৈষম্য", "example_sentence": "Without targeted intervention, the proliferation of automation risks entrenching systemic structural inequality between skilled and unskilled labour markets.", "band_level": "Band 9"},
                {"phrase": "comprehensive regulatory framework", "meaning_bn": "ব্যাপক নিয়ন্ত্রণমূলক কাঠামো বা নীতিমালা", "example_sentence": "Governments must establish a comprehensive regulatory framework to ensure that technological innovation proceeds responsibly and equitably.", "band_level": "Band 8.5"}
            ],
            "academic_synonyms": [
                {"basic": "increase", "advanced": "surge / escalate / proliferate / witness exponential growth", "context": "When describing data trends or societal changes"},
                {"basic": "decrease", "advanced": "plummet / dwindle / undergo a precipitous decline / contract sharply", "context": "Describing downward trends in data or social indicators"},
                {"basic": "important", "advanced": "paramount / indispensable / quintessential / of profound consequence", "context": "Evaluating significance in an academic argument"},
                {"basic": "problem", "advanced": "predicament / impediment / systemic challenge / pressing dilemma", "context": "Naming issues in Task 2 arguments"},
                {"basic": "show", "advanced": "illustrate / underscore / shed light on / attest to / corroborate", "context": "Referring to data or evidence in academic writing"}
            ],
            "cohesive_devices": [
                {"category": "Introducing an argument", "phrases": ["To begin with, it is noteworthy that", "Central to this discussion is", "A particularly salient point concerns"]},
                {"category": "Adding a supporting point", "phrases": ["Furthermore, it is equally imperative to recognise that", "Compounding this observation is the fact that", "Moreover, empirical evidence corroborates the view that"]},
                {"category": "Introducing contrast", "phrases": ["In stark contrast to this perspective", "Notwithstanding the aforementioned benefits", "Critics, however, contend that"]},
                {"category": "Concluding and synthesising", "phrases": ["Taking all factors into consideration, it is reasonable to deduce that", "In the final analysis, the weight of evidence suggests that", "It therefore follows that"]},
                {"category": "Giving examples", "phrases": ["A pertinent illustration of this is", "This is vividly exemplified by", "Empirical evidence for this can be found in"]}
            ]
        }

    # ── 4. PARAPHRASE ─────────────────────────────────────────────────────────

    def get_intro_paraphrases(self, task_type: str, prompt_statement: str) -> Dict[str, Any]:
        """Generate 3 Band 8+ paraphrased introductions with grammar pattern templates."""
        prompt = f"""You are a Cambridge IELTS Writing Examiner and Trainer (Band 9). Generate 3 distinct, fully written Band 8.5+ opening paraphrases for this IELTS prompt, plus 4 advanced grammar sentence templates.

Prompt: \"\"\"{prompt_statement}\"\"\"
Task Type: {task_type}

RULES:
- Each paraphrase must be 2 complete sentences total — do NOT copy any keyword from the original prompt.
- Use grammatical transformation: change active to passive, nouns to verbs, adjectives to noun phrases, etc.
- Each style must be genuinely distinct in grammar structure, not just word choice.
- The complex_sentence_starters must be fully written templates (with [SLOT] for student to fill in their own content).

Respond ONLY in valid JSON:
{{
  "paraphrase_options": [
    {{"style": "Cleft Sentence Structure (Band 8.5)", "text": "Fully written 2-sentence paraphrase using a cleft construction.", "grammar_note": "Brief note on the grammar transformation used"}},
    {{"style": "Passive Nominalization (Band 9)", "text": "Fully written 2-sentence paraphrase using passive voice and noun phrases.", "grammar_note": "Brief note on the grammar transformation used"}},
    {{"style": "Concessive Complex Clause (Band 9)", "text": "Fully written 2-sentence paraphrase using a concessive clause (While/Although/Whereas) + conditional or modal.", "grammar_note": "Brief note on the grammar transformation used"}}
  ],
  "complex_sentence_starters": [
    {{"type": "Subject-Verb Inversion (Band 9)", "template": "Not only does [YOUR CLAIM] generate [BENEFIT 1], but it also [BENEFIT 2], rendering it a matter of considerable societal significance."}},
    {{"type": "Participle Clause (Band 8.5)", "template": "Having examined [AREA OF EVIDENCE], it becomes increasingly evident that [YOUR POSITION] warrants more rigorous policy consideration."}},
    {{"type": "Hypothetical Conditional (Band 9)", "template": "Were [AUTHORITY / INSTITUTIONS] to implement [YOUR PROPOSED SOLUTION] systematically, the overarching challenge of [PROBLEM] would be substantially mitigated."}},
    {{"type": "Emphatic Fronting (Band 8.5)", "template": "It is precisely because of [ROOT CAUSE] that [YOUR TOPIC] has emerged as one of the most contentious contemporary debates."}}
  ]
}}"""

        try:
            raw = self._call(prompt, max_tokens=1800, temperature=0.35)
            data = self._parse_json(raw)
            if data and "paraphrase_options" in data:
                return data
        except Exception as e:
            logger.error(f"Paraphrase AI error: {e}")

        return {
            "paraphrase_options": [
                {"style": "Cleft Sentence Structure (Band 8.5)", "text": "It is the rapid, far-reaching transformation of modern societal structures that has thrust this particular question to the forefront of contemporary policy debate. This essay will argue that, while compelling objections exist, the preponderance of evidence firmly supports an affirmative position.", "grammar_note": "Cleft 'It is... that' construction shifts emphasis from subject to cause/reason."},
                {"style": "Passive Nominalization (Band 9)", "text": "The question of whether prevailing trends in this domain yield net benefits or cumulative harms has been a subject of sustained academic and public discourse in recent decades. In this essay, a position broadly in favour of regulated implementation will be advanced and substantiated.", "grammar_note": "Passive voice + nominalized verb phrases ('implementation', 'transformation') for academic register."},
                {"style": "Concessive Complex Clause (Band 9)", "text": "While a considerable body of scholarly opinion acknowledges the potential drawbacks associated with this development, a growing corpus of empirical evidence suggests that its transformative benefits considerably outweigh any attendant risks. This essay will examine both perspectives before arriving at a reasoned evaluative conclusion.", "grammar_note": "Concessive 'While...' clause + modal 'suggests that' to signal a nuanced, balanced position."}
            ],
            "complex_sentence_starters": [
                {"type": "Subject-Verb Inversion (Band 9)", "template": "Not only does [YOUR CLAIM] generate [BENEFIT 1], but it also [BENEFIT 2], rendering it a matter of considerable societal significance."},
                {"type": "Participle Clause (Band 8.5)", "template": "Having examined [AREA OF EVIDENCE], it becomes increasingly evident that [YOUR POSITION] warrants more rigorous policy consideration."},
                {"type": "Hypothetical Conditional (Band 9)", "template": "Were [AUTHORITY / INSTITUTIONS] to implement [YOUR PROPOSED SOLUTION] systematically, the overarching challenge of [PROBLEM] would be substantially mitigated."},
                {"type": "Emphatic Fronting (Band 8.5)", "template": "It is precisely because of [ROOT CAUSE] that [YOUR TOPIC] has emerged as one of the most contentious contemporary debates."}
            ]
        }

    # ── 5. POLISH SENTENCE ────────────────────────────────────────────────────

    def polish_sentence(self, sentence: str, task_type: str) -> Dict[str, Any]:
        """Upgrade a student draft sentence to Band 8.5+ with full diagnostic breakdown."""
        prompt = f"""You are a Cambridge IELTS Senior Examiner. A student has written the following sentence. Your job is to upgrade it to Band 8.5+ Lexical Resource and Grammatical Range, and explain exactly what was improved.

Student's original sentence:
\"\"\"{sentence}\"\"\"

Task Type: {task_type}

RULES:
- The band_8_version must be substantially different — not just a vocabulary swap. Use a more complex grammar structure.
- The band_6_diagnosis must identify specific weaknesses (e.g., basic vocabulary, simple SVO structure, repetition, informal register).
- Each key_upgrade must reference the specific original word/phrase AND the upgraded replacement.
- Limit to the 3 most impactful upgrades.

Respond ONLY in valid JSON, no markdown:
{{
  "original": "{sentence.replace(chr(34), chr(39))}",
  "band_6_diagnosis": "2-3 sentence specific diagnosis of what makes this a Band 6 sentence (mention specific words or structural issues)",
  "band_8_version": "Full rewritten Band 8.5+ sentence using advanced syntax and lexis",
  "alternative_version": "A second Band 8+ version using a different grammatical structure",
  "key_upgrades": [
    {{"from": "exact original word or phrase", "to": "advanced replacement", "why": "Specific reason: e.g., 'removes informal register', 'converts simple SVO to inversion', 'replaces basic verb with academic collocation'"}},
    {{"from": "exact original word or phrase", "to": "advanced replacement", "why": "Specific reason"}},
    {{"from": "exact original word or phrase", "to": "advanced replacement", "why": "Specific reason"}}
  ],
  "grammar_pattern_used": "Name of the grammar structure used in the Band 8 version (e.g., Non-finite participle clause, Subject-verb inversion, Passive nominalization)"
}}"""

        try:
            raw = self._call(prompt, max_tokens=1200, temperature=0.2)
            data = self._parse_json(raw)
            if data and "band_8_version" in data:
                return data
        except Exception as e:
            logger.error(f"Polish sentence AI error: {e}")

        return {
            "original": sentence,
            "band_6_diagnosis": "The sentence relies on basic Subject-Verb-Object structure with common vocabulary and an informal register, all of which limit the Lexical Resource and Grammatical Range scores.",
            "band_8_version": f"It is widely acknowledged by scholars and policymakers alike that {sentence.strip().rstrip('.').lower()}, a phenomenon that demands urgent and comprehensive regulatory attention.",
            "alternative_version": f"Having considered the available evidence, it becomes increasingly apparent that {sentence.strip().rstrip('.').lower()}, with significant implications for both individuals and broader societal structures.",
            "key_upgrades": [
                {"from": "basic phrasing", "to": "academic signposting construction", "why": "Cleft 'It is... that' structure raises GRA score by demonstrating syntactic range."},
                {"from": "simple verb", "to": "academic lexical collocation", "why": "Enhances Lexical Resource — shows awareness of academic register and collocation."},
                {"from": "plain conclusion", "to": "evaluative closing phrase", "why": "Demonstrates coherent argument development and adds C&C score."}
            ],
            "grammar_pattern_used": "Cleft Sentence (It is... that) + Relative Clause Extension"
        }

    # ── 6. TUTOR CHAT ─────────────────────────────────────────────────────────

    def tutor_chat(self, user_message: str, prompt_title: str, prompt_statement: str, student_essay_so_far: str) -> str:
        """Interactive ARIA Tutor — supports English and Bengali questions."""
        system = f"""You are ARIA — an expert, warm, and encouraging Cambridge IELTS Writing Coach (Band 9). You are helping a student in real-time during their writing exam practice session.

CURRENT EXAM CONTEXT:
- Prompt Topic: {prompt_title}
- Prompt Statement: {prompt_statement[:500]}
- Student's Current Draft (may be empty or partial):
\"\"\"{student_essay_so_far[:1500]}\"\"\"

COACHING RULES:
1. If the student writes in Bengali, reply in a MIX of Bengali explanation + English IELTS examples. Always keep IELTS terms (Band Descriptors, criteria names) in English.
2. Give SPECIFIC, actionable advice — not generic tips. Reference their actual draft when possible.
3. Structure your reply clearly: use short bullet points (•) or numbered steps.
4. Keep the reply under 200 words — they are in an exam and need fast, clear guidance.
5. ALWAYS end with one concrete Band 8+ example sentence relevant to their question.
6. Be encouraging and positive — build confidence."""

        try:
            return self._call(
                system + f"\n\nStudent's Question: {user_message}",
                max_tokens=900,
                temperature=0.45
            )
        except Exception as e:
            logger.error(f"Tutor chat AI error: {e}")
            return (
                "আরিয়া এখন উত্তর দিতে পারছে না — API সংযোগ পরীক্ষা করুন। তবে এই সাধারণ টিপটি মনে রাখুন:\n\n"
                "**Body Paragraph Formula (Band 8):**\n"
                "① Topic Sentence (main claim)\n"
                "② Elaboration (why / how it works)\n"
                "③ Example (specific, named evidence)\n"
                "④ Link back to thesis\n\n"
                "*Example:* 'Not only does digital education platforms democratise knowledge access, but they also eliminate the geographical constraints that have historically disadvantaged rural learners.'"
            )

    # ── UTILS ─────────────────────────────────────────────────────────────────

    def _parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        clean = text.strip()
        # Strip markdown fences
        for fence in ["```json", "```JSON", "```"]:
            if clean.startswith(fence):
                clean = clean[len(fence):]
                break
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()
        # Find the first { and last } to isolate JSON object
        start = clean.find("{")
        end = clean.rfind("}")
        if start != -1 and end != -1:
            clean = clean[start:end + 1]
        try:
            return json.loads(clean)
        except Exception as e:
            logger.warning(f"JSON parse failed: {e} — snippet: {clean[:200]}")
            return None
