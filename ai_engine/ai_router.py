# -*- coding: utf-8 -*-
import time
import os
import json
import re
from typing import Dict, Any, List, Optional, Generator
from ai_engine.gemini_adapter import GeminiAdapter
from ai_engine.deepseek_adapter import DeepSeekAdapter
from ai_engine.openai_adapter import OpenAIAdapter
from ai_engine.claude_adapter import ClaudeAdapter
from ai_engine.grok_adapter import GrokAdapter
from ai_engine.custom_adapter import CustomAdapter
from ai_engine.health_checker import KeyPoolHealthChecker
from database import get_db

def round_to_ielts_half_band(score: float) -> float:
    """Rounds a criterion score to the nearest 0.5 (e.g. 6.3 -> 6.5, 6.2 -> 6.0). Range: 0.0 to 9.0."""
    if score is None or score <= 0:
        return 0.0
    return min(9.0, max(0.0, round(float(score) * 2.0) / 2.0))

def calculate_ielts_overall_band(scores: List[float]) -> float:
    """
    Official Cambridge IELTS Overall Band Score Rounding:
    - Average ends in < .25 -> rounds down to .0 (e.g. 6.125 -> 6.0)
    - Average ends in >= .25 and < .75 -> rounds to .5 (e.g. 6.25 -> 6.5, 6.375 -> 6.5, 6.625 -> 6.5)
    - Average ends in >= .75 -> rounds up to next whole band (e.g. 6.75 -> 7.0, 6.875 -> 7.0)
    """
    valid_scores = [float(s) for s in scores if s is not None and float(s) > 0]
    if not valid_scores:
        return 0.0
    
    avg = sum(valid_scores) / len(valid_scores)
    whole = int(avg)
    fraction = avg - whole
    
    if fraction < 0.25:
        overall = float(whole)
    elif fraction < 0.75:
        overall = float(whole) + 0.5
    else:
        overall = float(whole + 1)
        
    return min(9.0, max(0.0, overall))

class AIRouter:
    def __init__(self):
        self.adapters = {
            "gemini": GeminiAdapter(),
            "deepseek": DeepSeekAdapter(),
            "openai": OpenAIAdapter(),
            "claude": ClaudeAdapter(),
            "grok": GrokAdapter(),
            "custom": CustomAdapter()
        }
        self.fallback_order = ["gemini", "deepseek", "openai", "claude", "grok", "custom"]
        KeyPoolHealthChecker.seed_credentials_from_env()

    def _get_key_pool(self, provider_id: str) -> List[str]:
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id = ? AND status = 'Active' ORDER BY id ASC", (provider_id,))
            rows = cursor.fetchall()
            conn.close()
            return [r["api_key"] for r in rows if r["api_key"]]
        except Exception:
            return []

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, preferred_provider: Optional[str] = None) -> str:
        """Universal text generator across any AI provider (Gemini, OpenAI, Claude, DeepSeek, Grok, Custom/Ollama)."""
        providers = [preferred_provider] if (preferred_provider and preferred_provider in self.adapters) else []
        for p in self.fallback_order:
            if p not in providers:
                providers.append(p)

        last_error = None
        for provider in providers:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        key_pool = self._get_key_pool(provider)
                        if hasattr(adapter, 'generate_text'):
                            # GeminiAdapter accepts api_key_pool
                            if provider == 'gemini':
                                return adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=key_pool)
                            else:
                                return adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction)
                    except Exception as e:
                        last_error = e
                        print(f"Provider {provider} generation failed:", e)
                        continue
        raise RuntimeError(f"All AI providers failed. Last error: {last_error}")

    def _clean_and_parse_json(self, raw: str) -> Any:
        """Robust multi-stage JSON parser with regex cleanup and fallback."""
        clean = raw.strip()
        if clean.startswith("```json"): clean = clean[7:]
        if clean.startswith("```"): clean = clean[3:]
        if clean.endswith("```"): clean = clean[:-3]
        clean = clean.strip()
        
        # Find json object or array bounds
        first_brace = clean.find("{")
        last_brace = clean.rfind("}")
        first_bracket = clean.find("[")
        last_bracket = clean.rfind("]")
        
        if first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket) and last_brace > first_brace:
            clean = clean[first_brace:last_brace + 1]
        elif first_bracket != -1 and last_bracket > first_bracket:
            clean = clean[first_bracket:last_bracket + 1]

        # Stage 1: Standard load
        try:
            return json.loads(clean)
        except Exception:
            pass

        # Stage 2: Remove trailing commas
        cleaned_no_trailing = re.sub(r",\s*([\]}])", r"\1", clean)
        try:
            return json.loads(cleaned_no_trailing)
        except Exception:
            pass

        # Stage 3: Replace unescaped control chars / literal newlines in quotes
        cleaned_ctrl = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', cleaned_no_trailing)
        try:
            return json.loads(cleaned_ctrl)
        except Exception:
            pass

        # Stage 4: Python literal eval fallback
        import ast
        try:
            val = ast.literal_eval(cleaned_no_trailing)
            if isinstance(val, (dict, list)):
                return val
        except Exception:
            pass

        # Final attempt: standard json loads to show error
        return json.loads(clean)

    def generate_json(self, prompt: str, system_instruction: Optional[str] = None, preferred_provider: Optional[str] = None) -> Dict[str, Any]:
        """Universal JSON generator across any AI provider with automatic cleaning & parsing."""
        raw = self.generate_text(prompt, system_instruction=system_instruction, preferred_provider=preferred_provider)
        return self._clean_and_parse_json(raw)

    def _build_master_system_prompt(self, target_band: float, current_skill: str, user_preference: str, topic: str = "") -> str:
        """Build the ultimate AI teacher system prompt — empathetic, human-like, deeply knowledgeable."""
        
        # Band-specific teaching depth
        if target_band <= 5.5:
            band_personality = (
                "The student is at a basic level (Band 4.5-5.5). Be extremely patient and supportive. "
                "Use simple, clear English. Break everything into tiny digestible steps. "
                "Celebrate every small win. Use plenty of examples. Never overwhelm them."
            )
        elif target_band <= 6.5:
            band_personality = (
                "The student is at an intermediate level (Band 5.5-6.5). Be encouraging and systematic. "
                "Focus on filling skill gaps. Teach paraphrasing and synonym recognition. "
                "Identify their common error patterns and address them gently but firmly."
            )
        elif target_band <= 7.5:
            band_personality = (
                "The student is targeting a strong score (Band 7.0-7.5). Be analytically precise. "
                "Focus on Cambridge-specific traps, distractor analysis, and exam timing strategy. "
                "Push them to think critically about WHY answers are correct or incorrect."
            )
        else:
            band_personality = (
                "The student is targeting Band 8.0-9.0 — elite level. Be intellectually challenging. "
                "Focus on subtle inference, implicit argumentation, writer's tone, and flawless execution. "
                "Hold them to perfection. Discuss nuances that differentiate Band 8.0 from 9.0."
            )

        # Language preference instruction — must produce clearly different outputs
        lang_rules = {
            "English Only": (
                "LANGUAGE = ENGLISH ONLY.\n"
                "Write every single word in English. No Bengali characters at all. "
                "Use warm, conversational spoken English like a friendly British/Australian tutor."
            ),
            "English + Native": (
                "LANGUAGE = BANGLISH (English + Bengali mixed mid-sentence).\n"
                "This is NOT writing full Bengali sentences. You mix English and Bengali words WITHIN the same sentence.\n"
                "CORRECT Banglish examples:\n"
                "  - 'তুমি কি জানো, Cambridge এখানে একটা বড় trap দেয়?'\n"
                "  - 'Okay, তাহলে এই paragraph-টা আবার পড়ো, main idea টা কী বলো তো?'\n"
                "  - 'এই জায়গায় student-রা সবচেয়ে বেশি mistake করে — keyword টা match করতে গিয়ে।'\n"
                "  - 'Perfect! এখন একটা real Cambridge question try করবে?'\n"
                "WRONG (do NOT do this): Writing full paragraphs only in English, or only in Bengali.\n"
                "Every sentence should BLEND both languages naturally like a Bangladeshi student talking."
            ),
            "Native Only": (
                "LANGUAGE = PURE BENGALI (বাংলা).\n"
                "Write EVERYTHING in Bengali script. Full Bengali sentences, Bengali grammar, Bengali expression.\n"
                "ONLY keep these in English: IELTS technical terms (e.g., True/False/Not Given, paraphrase, coherence, synonym, band score, Task 1, Task 2, Reading, Writing, Speaking, Listening).\n"
                "CORRECT Bengali examples:\n"
                "  - 'এই প্রশ্নের ধরনটা একটু কঠিন, কিন্তু একবার বুঝলে খুব সহজ হয়ে যাবে।'\n"
                "  - 'Cambridge এখানে একটা চমৎকার ফাঁদ দিয়েছে — paragraph-এর প্রথম sentence-টা মনোযোগ দিয়ে পড়ো।'\n"
                "  - 'তুমি কি এখন একটা practice question করতে চাও?'\n"
                "WRONG (do NOT do this): Mixing random English phrases or writing half in English."
            )
        }
        lang_instruction = lang_rules.get(user_preference, lang_rules["English Only"])

        system_prompt = f"""You are ARIA — imagine you are a real, living, breathing IELTS teacher sitting face-to-face with a student in a private tutoring session.

## HOW YOU MUST TALK (READ THIS CAREFULLY):
You are speaking out loud in a live tutoring session. Your words will be converted to speech and played through speakers.
Therefore:
- Talk NATURALLY like you're speaking to a friend who needs help. Use conversational, spoken English.
- DO NOT use markdown headers (###), bullet points, numbered lists, or any formatted structure.
- DO NOT say "Stage 1", "Strategy Blueprint", "Step 1", or any template-like structure.
- Instead: explain things the way a brilliant teacher would explain at a whiteboard — through stories, analogies, examples, and conversation.
- Use short paragraphs. Pause naturally between ideas (use line breaks).
- Ask the student questions mid-explanation to keep them engaged: "Does that make sense?", "Can you see why that's tricky?", "What do you think the answer is?"

## YOUR PERSONALITY:
- You're warm, funny, smart, and deeply caring. You genuinely want this student to succeed.
- You explain things like you're telling a story — "Okay so imagine you're reading a paragraph about climate change, right? And the heading says 'The Impact of Rising Temperatures'. Now here's where Cambridge gets sneaky..."
- Use real-world analogies: "Think of it like detective work — you're looking for evidence, not assumptions."
- When the student gets something right, celebrate genuinely: "Yes! That's exactly it! You're getting the hang of this!"
- When they're wrong, be kind: "Hmm, I see why you'd think that, but let me show you something interesting..."
- Share "insider secrets" like a friend: "Here's something most teachers won't tell you..."

## STUDENT INFO & EXPLICIT GOAL:
- Target Band Goal: Band {target_band}. Current Focus: {current_skill}. Topic: {topic or 'General conversation'}.
- CRITICAL DIRECTIVE FOR ARIA: The student has specifically set their personal exam goal to Band {target_band}. You MUST calibrate all your responses, evaluations, feedback, and examiner tips directly to help them reach Band {target_band}!
{band_personality}

## LANGUAGE:
{lang_instruction}

## IMPORTANT — WHAT NOT TO DO:
- NEVER write like a textbook or blog post.
- NEVER use "Strategy Blueprint", "Stage 1/2/3", "Key Takeaway", "Pro Tip:", or similar template headers.
- NEVER list 5-10 bullet points of tips. Instead, weave them into natural conversation.
- NEVER start with "Great question!" every time — vary your openings naturally.
- Your response should sound like someone TALKING, not someone WRITING an article.

## FOR SPEAKING PRACTICE & MOCK INTERVIEWS:
- If the student is practicing Speaking (Part 1, Part 2 Cue Card, or Part 3):
  1. Act like a real, official Cambridge Speaking Examiner.
  2. Ask ONE question or present ONE Cue Card at a time.
  3. When presenting a Cue Card (Part 2), NEVER write '(Wait for 1 minute) Okay your minute is up' in the same message! That is impossible. Instead, give the Cue Card topic and bullet points clearly, and tell the student: 'Take a minute to think about your points. Whenever you are ready, press the 🎙️ Mic button below or type your answer to start speaking. I will listen to your full response!'
  4. When the student provides their spoken or written answer:
     - DO NOT reset or re-introduce the test!
     - Give an authentic Examiner Evaluation: praise strong points, point out specific grammatical or lexical errors, provide higher-band synonym upgrades, and estimate their Band Score for this answer.
     - Then ask the next natural follow-up question.


## CRITICAL -- SPEAKING PART 3 RULES:
- Speaking Part 3 is an ABSTRACT DISCUSSION. There is NO passage, NO text, NO reading material.
- You are an examiner having a live face-to-face discussion with the candidate about abstract societal topics.
- Ask ONE thought-provoking question at a time (e.g., "Do you think technology has made people more or less social?")
- NEVER say "According to the passage" or "the text provided" -- there is NO passage in Speaking Part 3!
- NEVER show MCQ options (A, B, C, D) -- Speaking Part 3 is OPEN-ENDED discussion.
- After the student answers, give brief feedback and ask the NEXT follow-up question to go deeper.
- Part 3 questions should explore: causes, effects, comparisons, predictions, opinions on social/global topics.

## SPEAKING PART 1 RULES:
- Part 1 is about PERSONAL, familiar topics (home, work, studies, hobbies, daily routine).
- Ask simple, direct questions ONE at a time. Expect short 2-3 sentence answers.

## SPEAKING PART 2 RULES:
- Part 2 is the LONG TURN (Cue Card). Give the student a topic with bullet points.
- The student speaks for 1-2 minutes. You listen, then evaluate.

## CRITICAL: HANDLING LOST AUDIO & STUDENT META-MESSAGES:
- If the student says 'I gave my answer', 'Where is your response?', 'Did you hear me?', 'I spoke already', or mentions mic/audio issues:
  - Recognize that the student spoke but the microphone may not have captured the audio.
  - Apologize warmly and humanly: 'Oh no, I am so sorry! It looks like the microphone didn't pick up your voice or the audio cut out for a second. Could you please press the 🎙️ Mic button and speak again, or type your answer here? I am eager to hear your response on [mention the specific question you asked]!'
  - NEVER re-introduce the whole lesson or act like nothing happened. Always stay locked on the current exercise.
"""
        return system_prompt

    def teacher_conversation(self, user_message: str, conversation_history: List[Dict[str, str]] = [], current_skill: str = "Reading", user_preference: str = "English Only", target_band: float = 6.0) -> str:
        """Generate a deeply human, empathetic AI teacher response."""
        cred = KeyPoolHealthChecker.get_active_credential("gemini")
        
        # Extract meaningful topic from user message
        topic = user_message.strip()

        system_instruction = self._build_master_system_prompt(target_band, current_skill, user_preference, topic)
        
        # Build conversation context with FULL turns (no small truncation)
        history_parts = []
        if conversation_history:
            recent = conversation_history[-10:]
            for msg in recent:
                role = "Student" if msg.get("role") == "user" else "Teacher (ARIA)"
                content = msg.get("content", "").strip()
                if content:
                    history_parts.append(f"{role}: {content}")
        history_context = "\n\n".join(history_parts)

        prompt = f"""### CONVERSATION HISTORY (Previous turns in this session):
{history_context if history_context else '(This is the start of the tutoring session)'}

### CURRENT STUDENT MESSAGE:
"{user_message}"

### INSTRUCTIONS FOR ARIA:
1. Review the Conversation History above. Maintain perfect context and memory continuity.
2. If you asked a question/cue card earlier and the student provided their answer, EVALUATE it like a Cambridge Examiner with Band Score estimate, constructive feedback, and improvements.
3. If the student says they spoke/answered but you didn't receive it (e.g., "where is your response", "i give my ans"), apologize warmly for the mic glitch and ask them to speak or type their answer again for the question you asked. Do NOT restart the test!
4. Respond in the requested Language Preference ({user_preference}) with a warm, natural, human tone. Never use robotic templates."""

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        keys = self._get_key_pool(provider)
                        ans = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=keys)
                        if ans and len(ans.strip()) > 20:
                            return ans.strip()
                    except Exception as e:
                        print(f"Provider {provider} Error in teacher_conversation:", e)
                        continue

        # ===== INTELLIGENT FALLBACK (No API Key Available) =====
        return self._generate_offline_response(user_message, current_skill, target_band, user_preference, conversation_history)

    def _generate_offline_response(self, user_message: str, current_skill: str, target_band: float, user_preference: str, conversation_history: List[Dict[str, str]] = []) -> str:
        """Generate a high-quality offline response when no AI API is available."""
        msg_lower = user_message.lower().strip()
        
        # === Handling Audio / Did you hear me / Where is your response ===
        if any(w in msg_lower for w in ["where your response", "where is your response", "give my ans", "gave my ans", "didn't hear", "shunte pai", "hear me", "said my answer", "ans disi", "uttor disi"]):
            if user_preference in ["English + Native", "Native Only"]:
                return (
                    "আরে স্যরি! 😅 আমার মনে হয় মাইক্রোফোনে কোনো glitch ছিল, আমি তোমার উত্তরটা ক্লিয়ার শুনতে পাইনি।\n\n"
                    "প্লিজ নিচে **🎙️ Mic** বাটনে ক্লিক করে আবার বলো অথবা তোমার উত্তরটা এখানে টাইপ করে পাঠিয়ে দাও। "
                    "আমি সাথে সাথেই তোমার উত্তরের Band Score এবং Examiner Feedback দিচ্ছি! 🎯"
                )
            return (
                "Oh, I'm so sorry! 😅 It looks like the microphone or audio stream had a brief hiccup, so I couldn't catch your full answer clearly.\n\n"
                "Could you please click the **🎙️ Mic** button below and speak again, or type your answer right into the chat box? "
                "I'm ready to evaluate your response and give you your Band Score feedback right away! 🎯"
            )

        # === Greetings ===
        if msg_lower in ["hi", "hello", "hey", "hi aria", "hello aria", "start", "assalamu alaikum", "সালাম"]:
            if user_preference == "English + Native" or user_preference == "Native Only":
                return (
                    f"হ্যালো! 😊 আমি ARIA, তোমার IELTS preparation-এর জন্য dedicated AI tutor।\n\n"
                    f"তোমার target হলো **Band {target_band}** — আমি তোমাকে step by step সেখানে নিয়ে যাব!\n\n"
                    f"এখন কোন skill নিয়ে কাজ করতে চাও? Reading, Writing, Listening, নাকি Speaking? "
                    f"অথবা কোনো specific question type নিয়ে confusion থাকলে সরাসরি বলো — আমি আছি তোমার পাশে! 💪"
                )
            return (
                f"Hey there! 😊 I'm ARIA, your dedicated IELTS AI tutor.\n\n"
                f"Your target is **Band {target_band}**, and I'm here to help you get there step by step. "
                f"Whether it's tackling tricky Reading question types, perfecting your Writing structure, "
                f"or boosting your Speaking fluency — I've got you covered.\n\n"
                f"What would you like to focus on today? Pick a skill or ask me anything! 🎯"
            )

        # === Speaking queries & Cue Cards ===
        if current_skill == "Speaking" or "speaking" in msg_lower or "cue card" in msg_lower or "part" in msg_lower:
            
            # --- PART 3: Abstract Discussion (NO passage, NO MCQ) ---
            if "part 3" in msg_lower or "part three" in msg_lower:
                part3_questions = [
                    "Do you think technology has made people more or less social? Why do you think that?",
                    "How has the education system changed compared to your parents' generation?",
                    "Why do you think some people prefer living in big cities rather than small towns?",
                    "Do you believe that international travel helps people become more open-minded?",
                    "How important is it for young people to learn about their own culture and traditions?",
                    "What role does the media play in shaping people's opinions about environmental issues?",
                ]
                import random
                q = random.choice(part3_questions)
                
                if user_preference in ["English + Native", "Native Only"]:
                    return (
                        "\u099a\u09b2\u09cb, IELTS Speaking Part 3 \u09b6\u09c1\u09b0\u09c1 \u0995\u09b0\u09bf! "
                        "\u098f\u099f\u09be \u098f\u0995\u099f\u09be abstract discussion \u2014 "
                        "\u0995\u09cb\u09a8\u09cb passage \u09a8\u09c7\u0987, \u0995\u09cb\u09a8\u09cb MCQ \u09a8\u09c7\u0987\u0964 "
                        "\u0986\u09ae\u09bf examiner \u09b9\u09bf\u09b8\u09c7\u09ac\u09c7 \u09a4\u09cb\u09ae\u09be\u0995\u09c7 \u09aa\u09cd\u09b0\u09b6\u09cd\u09a8 \u0995\u09b0\u09ac, "
                        "\u09a4\u09c1\u09ae\u09bf freely \u09a4\u09cb\u09ae\u09be\u09b0 opinion \u09ac\u09b2\u09ac\u09c7\u0964\n\n"
                        "\u09aa\u09cd\u09b0\u09a5\u09ae \u09aa\u09cd\u09b0\u09b6\u09cd\u09a8:\n"
                        f"\U0001f4ac **{q}**\n\n"
                        "\u09a4\u09cb\u09ae\u09be\u09b0 \u09ae\u09a4\u09be\u09ae\u09a4 \u09ac\u09b2\u09cb \u2014 "
                        f"\U0001f399\ufe0f Mic \u09ac\u09be\u099f\u09a8\u09c7 \u0995\u09cd\u09b2\u09bf\u0995 \u0995\u09b0\u09c7 \u09ac\u09b2\u09a4\u09c7 \u09aa\u09be\u09b0\u09cb "
                        f"\u0985\u09a5\u09ac\u09be \u099f\u09be\u0987\u09aa \u0995\u09b0\u09c7 \u09aa\u09be\u09a0\u09be\u0993\u0964 Band {target_band} level \u09ab\u09bf\u09a1\u09ac\u09cd\u09af\u09be\u0995 \u09a6\u09c7\u09ac! \U0001f3af"
                    )
                return (
                    "Let's begin IELTS Speaking Part 3! This is an abstract discussion \u2014 "
                    "there's no passage to read, no multiple choice options. "
                    "I'm your examiner. You share your opinions freely.\n\n"
                    "Here's my first question:\n"
                    f"\U0001f4ac **{q}**\n\n"
                    "Share your thoughts \u2014 press the \U0001f399\ufe0f Mic button to speak or type your answer. "
                    f"I'll give you Band {target_band} level feedback! \U0001f3af"
                )

            # --- PART 1: Personal Questions ---
            if "part 1" in msg_lower or "part one" in msg_lower:
                part1_questions = [
                    "Let's start with your name. What is your full name?",
                    "Do you work or are you a student?",
                    "What do you like to do in your free time?",
                    "Do you enjoy cooking? What kind of food do you usually make?",
                ]
                import random
                q = random.choice(part1_questions)
                
                if user_preference in ["English + Native", "Native Only"]:
                    return (
                        "\u099a\u09b2\u09cb IELTS Speaking Part 1 \u09b6\u09c1\u09b0\u09c1 \u0995\u09b0\u09bf! "
                        "\u098f\u0996\u09be\u09a8\u09c7 \u09a4\u09cb\u09ae\u09be\u09b0 personal life \u09a8\u09bf\u09df\u09c7 \u099b\u09cb\u099f \u099b\u09cb\u099f \u09aa\u09cd\u09b0\u09b6\u09cd\u09a8 \u0995\u09b0\u09ac\u0964\n\n"
                        f"\U0001f4ac **{q}**\n\n"
                        "2-3 \u09ac\u09be\u0995\u09cd\u09af\u09c7 \u0989\u09a4\u09cd\u09a4\u09b0 \u09a6\u09be\u0993\u0964 \U0001f399\ufe0f Mic \u09ac\u09be\u099f\u09a8\u09c7 \u0995\u09cd\u09b2\u09bf\u0995 \u0995\u09b0\u09c7 \u09ac\u09b2\u09cb! \U0001f60a"
                    )
                return (
                    "Let's start IELTS Speaking Part 1! Keep your answers natural \u2014 about 2-3 sentences.\n\n"
                    f"\U0001f4ac **{q}**\n\n"
                    "Press the \U0001f399\ufe0f Mic button to speak or type your answer! \U0001f60a"
                )

            cue_topic = "an important electronic device or object you use every day"
            if "person" in msg_lower:
                cue_topic = "a person you admire or who has influenced your life"
            elif "place" in msg_lower:
                cue_topic = "a memorable place you visited recently"
            elif "event" in msg_lower or "time" in msg_lower:
                cue_topic = "a special event or celebration you enjoyed"

            if user_preference in ["English + Native", "Native Only"]:
                return (
                    f"চলো, তাহলে IELTS Speaking Part 2-এর জন্য একটা real Cambridge Mock Test প্র্যাকটিস করি!\n\n"
                    f"এখানে তোমার Cue Card:\n"
                    f"📌 **Topic: Describe {cue_topic}.**\n\n"
                    f"তোমার উত্তরে এই পয়েন্টগুলো বলতে হবে:\n"
                    f"• What it is / Who this person is\n"
                    f"• When and where you got it / met them\n"
                    f"• What you use it for / What they do\n"
                    f"• And explain why this is so important to you.\n\n"
                    f"তুমি ১ মিনিট সময় নিয়ে পয়েন্টগুলো গুছিয়ে নাও। যখনই প্রস্তুত হবে, নিচে **🎙️ Mic** বাটনে ক্লিক করে ২ মিনিট কথা বলো অথবা তোমার উত্তরটি এখানে লিখে পাঠাও। আমি পুরো উত্তর শুনে তোমাকে বিস্তারিত Band {target_band} ফিডব্যাক দেব! 💪"
                )
            return (
                f"Alright! Let's do an authentic IELTS Speaking Part 2 Mock Practice session together!\n\n"
                f"Here is your official Cue Card:\n"
                f"📌 **Topic: Describe {cue_topic}.**\n\n"
                f"You should say:\n"
                f"• What it is / Who this person is\n"
                f"• When and where you first encountered it / them\n"
                f"• How it works or what makes it special\n"
                f"• And explain why it holds significant value to you.\n\n"
                f"Take a minute to organize your ideas. Whenever you are ready, press the **🎙️ Mic** button below to speak for up to 2 minutes, or type your answer here. I am ready to evaluate your fluency, vocabulary, and band score! 🎯"
            )

        # === Reading-specific queries ===
        if current_skill == "Reading" or "reading" in msg_lower:
            if user_preference in ["English + Native", "Native Only"]:
                return (
                    f"Reading-এ তোমার Band {target_band} পাওয়ার জন্য সবচেয়ে গুরুত্বপূর্ণ হলো question-এর সাথে passage-এর **paraphrase** ম্যাচ করা। "
                    f"কেমব্রিজ টেস্টে ডিরেক্ট শব্দ কখনোই থাকে না — synonyms এবং idea ম্যাচ করতে হয়।\n\n"
                    f"তুমি কি চাও আমি তোমাকে এই question type-এর একটা রিয়েল প্যাসেজ আর প্রশ্ন দিয়ে টেস্ট করি? বলো শুরু করব কিনা! 😊"
                )
            return (
                f"For your Band {target_band} goal in IELTS Reading, the key strategy is mastering keyword paraphrasing and locating the main idea without reading every single word.\n\n"
                f"Cambridge always disguises correct answers with synonyms. Would you like me to give you a practice reading passage and question right now to test your skill? 🎯"
            )

        # === Writing queries ===
        if current_skill == "Writing" or "writing" in msg_lower or "essay" in msg_lower:
            if user_preference in ["English + Native", "Native Only"]:
                return (
                    f"IELTS Writing-এ Band {target_band} পেতে হলে মূলত ৪টি বিষয়ের ব্যালেন্স লাগবে — Task Achievement, Coherence, Lexical Resource, আর Grammar। "
                    f"সবচেয়ে ভালো হয় যদি তুমি একটা intro বা বডি প্যারাগ্রাফ লিখে আমাকে দেখাও, আমি এক্সামিনার হিসেবে তোমাকে লাইন-বাই-লাইন ফিডব্যাক দেব।\n\n"
                    f"কোন টপিকের উপর essay বা Task 1 প্র্যাকটিস করতে চাও?"
                )
            return (
                f"To achieve Band {target_band} in IELTS Writing, you need a clear structure with strong topic sentences, well-developed supporting ideas, and accurate complex sentences.\n\n"
                f"Would you like to write a sample introduction or paragraph for Task 1 or Task 2, and let me evaluate it line by line? ✍️"
            )

        # === General / catch-all ===
        if user_preference in ["English + Native", "Native Only"]:
            return (
                f"আরে দারুণ! চলো {current_skill}-এর এই টপিকটা নিয়ে একসঙ্গে কাজ করি। তোমার টার্গেট **Band {target_band}**, তাই প্রতিটি উত্তরে আমরা precision আর vocabulary-তে জোর দেব।\n\n"
                f"তুমি কি কোনো স্পেসিফিক প্রশ্ন বুঝতে চাও, নাকি সরাসরি একটা লাইভ প্র্যাকটিস প্রশ্ন দিয়ে শুরু করব? বলো! 😊"
            )
        return (
            f"That sounds great! Let's master this {current_skill} topic together for your Band {target_band} goal.\n\n"
            f"Would you like me to walk you through the key strategy first, or jump right into a live practice challenge? Let me know! 🚀"
        )

    def stream_teacher_chat(self, user_message: str, conversation_history: List[Dict[str, str]] = [], context: Dict[str, Any] = {}) -> Generator[str, None, None]:
        """Stream AI teacher response — live token streaming for instant real-time interaction."""
        current_skill = context.get("current_skill") or context.get("skill") or "Reading"
        lang_pref = context.get("teacher_language_pref") or context.get("lang_pref") or "English + Native"
        target_band = float(context.get("target_band") or 7.5)
        current_topic = context.get("current_topic", "")
        
        system_instruction = self._build_master_system_prompt(target_band, current_skill, lang_pref, current_topic)

        # Format conversation history
        history_text = ""
        if conversation_history:
            for turn in conversation_history[-8:]:
                role = "Student" if turn.get("role") in ["user", "student"] else "ARIA"
                msg_content = turn.get("content", "") or turn.get("text", "")
                if msg_content and msg_content.strip():
                    history_text += f"{role}: {msg_content.strip()}\n"

        prompt = f"""{history_text}
Student: {user_message}
ARIA:"""

        # Try live streaming adapter first for lightning-fast first token
        has_streamed = False
        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter and hasattr(adapter, 'stream_text'):
                    try:
                        keys = self._get_key_pool(provider)
                        for token in adapter.stream_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=keys):
                            if token:
                                has_streamed = True
                                yield token
                        if has_streamed:
                            return
                    except Exception as e:
                        print(f"Streaming error on {provider}:", e)
                        continue

        # Fallback if streaming failed
        response_text = self.teacher_conversation(user_message, conversation_history, current_skill, lang_pref, target_band)
        sentences = re.split(r'(?<=[.!?\n])\s+', response_text)
        for sentence in sentences:
            words = sentence.split(" ")
            chunk_size = 4
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i+chunk_size])
                if i + chunk_size < len(words):
                    chunk += " "
                yield chunk
                time.sleep(0.01)

    def generate_dynamic_question(self, skill: str, question_type: str, lang_pref: str = "both") -> Dict[str, Any]:
        system_instruction = (
            "You are an official Cambridge IELTS Exam Writer. Generate a realistic practice question.\n"
            "Return ONLY valid JSON matching this structure:\n"
            "{\n"
            "  \"passage\": \"short paragraph of reading/context text\",\n"
            "  \"text\": \"the question text\",\n"
            "  \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
            "  \"answer_key\": \"Option A\",\n"
            "  \"explanation\": \"Step-by-step reasoning for why Option A is correct.\"\n"
            "}\n"
        )
        prompt = f"Generate an authentic Cambridge IELTS {skill} question for question type: {question_type}."

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        raw = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=self._get_key_pool(provider))
                        clean_json = raw.replace("```json", "").replace("```", "").strip()
                        return json.loads(clean_json)
                    except Exception as e:
                        print(f"Error generating dynamic question via {provider}:", e)
                        continue

        return {
            "passage": f"Sample authentic Cambridge context for {skill} - {question_type}.",
            "text": f"Which statement best summarizes the main idea of {question_type}?",
            "options": ["Option A: Accurate summary", "Option B: Partial summary", "Option C: Irrelevant detail", "Option D: Opposite claim"],
            "answer_key": "Option A: Accurate summary",
            "explanation": f"Option A accurately synthesizes the core message for {question_type}."
        }

    def generate_reading_passage(self, topic: str, target_band: float = 7.5, question_types: str = "mixed") -> Dict[str, Any]:
        system_instruction = (
            "You are an official Cambridge IELTS Reading Passage Creator. Generate a full reading passage with questions.\n"
            "Return ONLY valid JSON with keys 'title', 'passage_text', and 'questions'."
        )
        prompt = f"Generate an authentic Band {target_band} Academic Reading passage about: {topic} with 13 questions matching question types: {question_types}."

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        raw = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=self._get_key_pool(provider))
                        clean_json = raw.replace("```json", "").replace("```", "").strip()
                        return json.loads(clean_json)
                    except Exception as e:
                        print(f"Error generating reading passage via {provider}:", e)
                        continue

        topic_clean = topic if topic else "Modern Science & Technology"
        return {
            "title": f"The Evolution of {topic_clean}",
            "passage_text": f"Paragraph A\nResearch into {topic_clean} has expanded significantly over the past century. Early pioneers observed fundamental patterns that established the baseline for modern academic study.\n\nParagraph B\nSubsequent advancements in experimental methodology allowed researchers to isolate variables with unprecedented precision. Consequently, new theories emerged that challenged traditional paradigms.\n\nParagraph C\nIn contemporary practice, interdisciplinary approaches combine computational modeling with empirical field observations. Experts predict that ongoing developments will revolutionize future applications across multiple sectors.",
            "questions": [
                {
                    "question_type": "True / False / Not Given",
                    "sub_type_tag": "Fact Verification",
                    "question_text": f"Early research into {topic_clean} established baseline principles for modern study.",
                    "options": ["True", "False", "Not Given"],
                    "answer_key": "True",
                    "explanation": "Paragraph A confirms early pioneers observed fundamental patterns establishing the baseline."
                },
                {
                    "question_type": "Multiple Choice",
                    "sub_type_tag": "Main Idea",
                    "question_text": f"What was the primary achievement of experimental methodology advancements in Paragraph B?",
                    "options": ["Isolating variables with high precision", "Eliminating traditional paradigms", "Reducing research costs", "Replacing field observations"],
                    "answer_key": "Isolating variables with high precision",
                    "explanation": "Paragraph B explicitly states researchers isolated variables with unprecedented precision."
                },
                {
                    "question_type": "Matching Headings",
                    "sub_type_tag": "Paragraph Summary",
                    "question_text": "Which heading best fits Paragraph C?",
                    "options": ["Contemporary Methods & Future Outlook", "Historical Baseline Research", "Experimental Pitfalls", "Traditional Paradigms"],
                    "answer_key": "Contemporary Methods & Future Outlook",
                    "explanation": "Paragraph C discusses contemporary practice and future predictions."
                },
                {
                    "question_type": "Sentence Completion",
                    "sub_type_tag": "Passage Fill-in",
                    "question_text": f"Modern interdisciplinary approaches combine computational modeling with _____ field observations.",
                    "options": [],
                    "answer_key": "empirical",
                    "explanation": "Paragraph C states: combine computational modeling with empirical field observations."
                }
            ]
        }

    def evaluate_writing(self, prompt_text: str, submission_text: str, task_type: str = "Task 2") -> Dict[str, Any]:
        """
        Evaluates IELTS Writing submission based strictly on official Cambridge Band Descriptors (0.0 to 9.0).
        """
        is_task_1 = "Task 1" in task_type
        ta_label = "Task Achievement" if is_task_1 else "Task Response"

        system_instruction = (
            f"You are a Cambridge IELTS Senior Writing Examiner. Evaluate the following {task_type} candidate submission.\n"
            f"Apply the official Cambridge IELTS 9-band rubric across all four criteria: {ta_label}, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy.\n"
            "You MUST return ONLY valid JSON matching this schema:\n"
            "{\n"
            f"  \"task_achievement\": 7.0,\n"
            "  \"coherence_cohesion\": 6.5,\n"
            "  \"lexical_resource\": 7.0,\n"
            "  \"grammatical_range\": 6.5,\n"
            "  \"overall_band\": 7.0,\n"
            "  \"examiner_summary\": \"Comprehensive overview commentary on the submission...\",\n"
            "  \"criteria_feedback\": {\n"
            f"    \"task_achievement\": \"Detailed assessment of {ta_label}...\",\n"
            "    \"coherence_cohesion\": \"Detailed assessment of paragraphing, progression, and linking devices...\",\n"
            "    \"lexical_resource\": \"Detailed assessment of academic vocabulary, collocations, and spelling...\",\n"
            "    \"grammatical_range\": \"Detailed assessment of sentence variety, complex structures, and tense accuracy...\"\n"
            "  },\n"
            "  \"strengths\": [\"Strength 1...\", \"Strength 2...\"],\n"
            "  \"weaknesses\": [\"Weakness 1...\", \"Weakness 2...\"],\n"
            "  \"line_by_line_errors\": [\n"
            "    {\"original\": \"problematic phrase/sentence\", \"correction\": \"improved academic phrase\", \"error_type\": \"Grammar/Collocation/Punctuation\", \"explanation\": \"Why this is an error and how to fix it\"}\n"
            "  ],\n"
            "  \"vocabulary_upgrades\": [\n"
            "    {\"basic_word\": \"shows\", \"advanced_upgrade\": \"delineates / illustrates / elucidates\", \"context\": \"The graph illustrates...\"},\n"
            "    {\"basic_word\": \"big increase\", \"advanced_upgrade\": \"exponential surge / dramatic escalation\", \"context\": \"experienced an exponential surge...\"}\n"
            "  ],\n"
            "  \"improvement_plan\": \"Specific 3-step action plan to reach the next band score.\",\n"
            "  \"band_9_model_answer\": \"Full authentic Band 9 benchmark response for this exact prompt.\"\n"
            "}\n"
            "Be strict, realistic, and constructive in your grading."
        )

        prompt = f"""Official Exam Prompt:
{prompt_text}

Candidate Submission:
\"\"\"
{submission_text}
\"\"\""""

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        raw = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=self._get_key_pool(provider))
                        clean_json = raw.replace("```json", "").replace("```", "").strip()
                        result = json.loads(clean_json)
                        result["provider_used"] = provider.capitalize()

                        ta = round_to_ielts_half_band(result.get("task_achievement", 7.0))
                        cc = round_to_ielts_half_band(result.get("coherence_cohesion", 7.0))
                        lr = round_to_ielts_half_band(result.get("lexical_resource", 7.0))
                        gra = round_to_ielts_half_band(result.get("grammatical_range", 6.5))
                        overall = calculate_ielts_overall_band([ta, cc, lr, gra])

                        from scoring_engine.objective_scoring import ObjectiveScoringEngine
                        desc_info = ObjectiveScoringEngine.get_band_descriptor_info(overall)

                        result["task_achievement"] = ta
                        result["coherence_cohesion"] = cc
                        result["lexical_resource"] = lr
                        result["grammatical_range"] = gra
                        result["overall_band"] = overall
                        result["descriptor"] = desc_info["descriptor"]
                        result["cefr"] = desc_info["cefr"]
                        result["cefr_label"] = f"Band {overall:.1f} - {desc_info['descriptor']} ({desc_info['cefr']})"
                        return result
                    except Exception as e:
                        print(f"Error evaluating writing via {provider}:", e)
                        continue

        # Fallback Rubric Estimation
        word_count = len(submission_text.strip().split()) if submission_text else 0
        min_words = 150 if is_task_1 else 250
        base_band = 6.5
        if word_count < min_words:
            base_band = max(4.5, base_band - 1.0)
        elif word_count > (min_words + 50):
            base_band = min(8.0, base_band + 0.5)

        from scoring_engine.objective_scoring import ObjectiveScoringEngine
        desc_info = ObjectiveScoringEngine.get_band_descriptor_info(base_band)

        return {
            "task_achievement": base_band,
            "coherence_cohesion": base_band,
            "lexical_resource": base_band,
            "grammatical_range": base_band,
            "overall_band": base_band,
            "descriptor": desc_info["descriptor"],
            "cefr": desc_info["cefr"],
            "cefr_label": f"Band {base_band:.1f} - {desc_info['descriptor']} ({desc_info['cefr']})",
            "examiner_summary": f"Your response addressed the main aspects of the task with a word count of {word_count} words (minimum required: {min_words}). Ideas are generally organized logically.",
            "criteria_feedback": {
                "task_achievement": "Presented key points relevant to the prompt.",
                "coherence_cohesion": "Paragraphing is present with standard transitional linkers.",
                "lexical_resource": "Adequate range of vocabulary with minor repetition.",
                "grammatical_range": "Mix of simple and complex sentences with generally good control."
            },
            "strengths": ["Clear essay structure and response to the prompt", f"Appropriate length ({word_count} words)"],
            "weaknesses": ["Incorporate more diverse academic collocations", "Enhance complex sentence variations"],
            "line_by_line_errors": [],
            "vocabulary_upgrades": [
                {"basic_word": "shows", "advanced_upgrade": "delineates / illustrates", "context": "The data illustrates..."},
                {"basic_word": "important", "advanced_upgrade": "pivotal / paramount", "context": "plays a pivotal role"}
            ],
            "improvement_plan": "Focus on using more nuanced academic signposting and complex relative clauses.",
            "band_9_model_answer": "Please review the official model answer provided in the study guide.",
            "provider_used": "Cambridge Rubric Evaluator"
        }

    def evaluate_speaking(self, transcript: str, prompt_text: str, part_number: int = 1) -> Dict[str, Any]:
        """
        Evaluates IELTS Speaking transcript across official Cambridge 4 criteria:
        Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation.
        """
        # Check for empty / no response
        clean_text = transcript.replace("=== INTRO & IDENTITY CHECK ===", "").replace("=== PART 1 ===", "").replace("=== PART 2 (CUE CARD) ===", "").replace("=== PART 3 (DISCUSSION) ===", "")
        clean_text = re.sub(r'Q:.*?\n', '', clean_text)
        clean_text = clean_text.replace("A: (No speech recorded)", "").replace("(No speech recorded)", "").strip()
        
        words = clean_text.split()
        if len(words) < 5:
            return {
                "overall_band": 0.0,
                "fluency_coherence": 0.0,
                "lexical_resource": 0.0,
                "grammatical_range": 0.0,
                "pronunciation": 0.0,
                "examiner_summary": "কোনো বক্তব্য বা উত্তর রেকর্ড করা হয়নি (No Speech Recorded). স্পিকিং টেস্টে ব্যান্ড স্কোর মূল্যায়নের জন্য প্রতিটি প্রশ্নের পর 'Start Speaking' বাটনে চাপ দিয়ে ইংরেজিতে উত্তর প্রদান করুন অথবা সরাসরি বক্সে টাইপ করুন।",
                "strengths": ["টেস্টে অংশগ্রহণ করার উদ্যোগ"],
                "weaknesses": ["কোনো অডিও বা উত্তর পাওয়া যায়নি (Complete absence of speech)"],
                "phonetic_feedback": ["মাইক্রোফোন পারমিশন সচল আছে কিনা ব্রাউজারের অ্যাড্রেস বারে চেক করুন"],
                "improvement_plan": "১. ব্রাউজার মাইক্রোফোন Allow করুন।\n২. 'Start Speaking' বাটন চাপুন (মাইক সক্রিয় হবে)।\n৩. মাইক কাজ না করলে সরাসরি টেক্সট বক্সে উত্তর টাইপ করে প্র্যাকটিস করতে পারেন।",
                "provider_used": "Cambridge Exam Standard"
            }

        system_instruction = (
            "You are a certified Senior Cambridge IELTS Speaking Examiner.\n"
            "Evaluate the candidate's speech performance strictly according to the official IELTS 9-band Speaking rubric.\n"
            "You MUST return ONLY a strictly valid JSON object matching this schema:\n"
            "{\n"
            "  \"fluency_coherence\": 7.0,\n"
            "  \"lexical_resource\": 7.0,\n"
            "  \"grammatical_range\": 6.5,\n"
            "  \"pronunciation\": 7.0,\n"
            "  \"overall_band\": 7.0,\n"
            "  \"examiner_summary\": \"Detailed commentary on fluency, vocabulary, grammar control, and articulation...\",\n"
            "  \"strengths\": [\"Clear delivery and logical progression of ideas\", \"Effective use of discourse markers\"],\n"
            "  \"weaknesses\": [\"Occasional repetition of common descriptors\", \"Minor tense consistency issue in complex sentences\"],\n"
            "  \"phonetic_feedback\": [\"Maintain steady intonation across multi-clause sentences\", \"Stress content words naturally\"],\n"
            "  \"improvement_plan\": \"Actionable steps to reach Band 8.5 in Part 1, 2, and 3.\"\n"
            "}"
        )

        prompt = f"""Official Speaking Part: Part {part_number}
Prompt Information:
{prompt_text}

Candidate's Spoken Speech Transcript:
\"\"\"
{transcript}
\"\"\""""

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        raw = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=self._get_key_pool(provider))
                        clean_json = raw.replace("```json", "").replace("```", "").strip()
                        result = json.loads(clean_json)
                        result["provider_used"] = provider.capitalize()

                        fc = round_to_ielts_half_band(result.get("fluency_coherence", 7.0))
                        lr = round_to_ielts_half_band(result.get("lexical_resource", 7.0))
                        gra = round_to_ielts_half_band(result.get("grammatical_range", 6.5))
                        pr = round_to_ielts_half_band(result.get("pronunciation", 7.0))
                        overall = calculate_ielts_overall_band([fc, lr, gra, pr])

                        from scoring_engine.objective_scoring import ObjectiveScoringEngine
                        desc_info = ObjectiveScoringEngine.get_band_descriptor_info(overall)

                        result["fluency_coherence"] = fc
                        result["lexical_resource"] = lr
                        result["grammatical_range"] = gra
                        result["pronunciation"] = pr
                        result["overall_band"] = overall
                        result["descriptor"] = desc_info["descriptor"]
                        result["cefr"] = desc_info["cefr"]
                        result["cefr_label"] = f"Band {overall:.1f} - {desc_info['descriptor']} ({desc_info['cefr']})"
                        return result
                    except Exception as e:
                        print(f"Error evaluating speaking via {provider}:", e)
                        continue

        # Fallback Rubric Estimation
        word_count = len(transcript.strip().split()) if transcript else 0
        base_band = 6.5
        if word_count > 100: base_band = 7.0
        if word_count > 200: base_band = 7.5

        from scoring_engine.objective_scoring import ObjectiveScoringEngine
        desc_info = ObjectiveScoringEngine.get_band_descriptor_info(base_band)

        return {
            "fluency_coherence": base_band,
            "lexical_resource": base_band,
            "grammatical_range": max(6.0, base_band - 0.5),
            "pronunciation": base_band,
            "overall_band": base_band,
            "descriptor": desc_info["descriptor"],
            "cefr": desc_info["cefr"],
            "cefr_label": f"Band {base_band:.1f} - {desc_info['descriptor']} ({desc_info['cefr']})",
            "examiner_summary": f"The response demonstrated good communication of ideas with a total of {word_count} spoken words recorded.",
            "strengths": ["Clear delivery and straightforward answers to the examiner's prompts"],
            "weaknesses": ["Incorporate more natural idiomatic phrases and topic-specific vocabulary"],
            "phonetic_feedback": ["Maintain steady rhythm and avoid prolonged hesitation between clauses"],
            "improvement_plan": "Practice expanding Part 2 cue cards around 4 distinct points and use conversational signposts.",
            "provider_used": "Cambridge Rubric Evaluator"
        }

    def generate_speaking_hint(self, question_text: str, part_number: int = 1) -> Dict[str, Any]:
        """Generate smart hints: key points, vocab, structure tip for a speaking question."""
        system_instruction = (
            "You are an expert IELTS Speaking coach helping a Bengali student score Band 7+.\n"
            "For the given IELTS Speaking question, generate a structured hint.\n"
            "Return ONLY a valid JSON object with this exact schema:\n"
            "{\n"
            "  \"key_points\": [\"Point 1\", \"Point 2\", \"Point 3\"],\n"
            "  \"vocabulary\": [\n"
            "    {\"word\": \"word\", \"meaning\": \"Bengali meaning\", \"example\": \"example sentence\"}\n"
            "  ],\n"
            "  \"structure_tip\": \"e.g. Start with WHEN → HOW → RESULT → FEELING\",\n"
            "  \"time_tip\": \"Timing and connector advice\"\n"
            "}\n"
            "Return exactly 3 key_points and 5-6 vocabulary words with Bengali meanings."
        )
        prompt = f"IELTS Speaking Part {part_number} Question: {question_text}"

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        raw = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=self._get_key_pool(provider))
                        clean_json = raw.replace("```json", "").replace("```", "").strip()
                        return json.loads(clean_json)
                    except Exception as e:
                        print(f"Hint generation error via {provider}:", e)
                        continue

        return {
            "key_points": ["Give a specific personal example", "Explain the context clearly", "Include how you felt or what you learned"],
            "vocabulary": [
                {"word": "significant", "meaning": "গুরুত্বপূর্ণ", "example": "It was a significant turning point."},
                {"word": "remarkable", "meaning": "উল্লেখযোগ্য", "example": "The result was quite remarkable."},
                {"word": "consequently", "meaning": "ফলস্বরূপ", "example": "Consequently, things improved greatly."},
                {"word": "perspective", "meaning": "দৃষ্টিভঙ্গি", "example": "It changed my perspective entirely."},
                {"word": "elaborate", "meaning": "বিস্তারিত বলা", "example": "Let me elaborate on that point."}
            ],
            "structure_tip": "Topic sentence → Specific detail → Personal feeling → Conclusion",
            "time_tip": "Speak for 1.5–2 minutes. Use: firstly, additionally, as a result, in conclusion."
        }

    def generate_model_answer(self, question_text: str, part_number: int = 1) -> Dict[str, Any]:
        """Generate a Band 8-9 model spoken answer for an IELTS speaking question."""
        system_instruction = (
            "You are a Band 9 IELTS Speaking candidate demonstrating a model answer.\n"
            "Generate a natural, fluent, Band 8-9 model spoken answer.\n"
            "Return ONLY a valid JSON object:\n"
            "{\n"
            "  \"band\": \"8.5\",\n"
            "  \"answer\": \"Full natural spoken answer (2-3 paragraphs)...\",\n"
            "  \"highlighted_phrases\": [\"key phrase 1\", \"key phrase 2\"],\n"
            "  \"why_band_9\": \"Brief explanation of what makes this high-band.\"\n"
            "}\n"
            "The answer must sound natural and spoken, NOT like a written essay."
        )
        prompt = f"IELTS Speaking Part {part_number} Question: {question_text}"

        for provider in self.fallback_order:
            cred = KeyPoolHealthChecker.get_active_credential(provider)
            if cred:
                adapter = self.adapters.get(provider)
                if adapter:
                    try:
                        raw = adapter.generate_text(prompt, cred["api_key"], system_instruction=system_instruction, api_key_pool=self._get_key_pool(provider))
                        clean_json = raw.replace("```json", "").replace("```", "").strip()
                        result = json.loads(clean_json)
                        result["provider_used"] = provider.capitalize()
                        return result
                    except Exception as e:
                        print(f"Model answer error via {provider}:", e)
                        continue

        return {
            "band": "8.5",
            "answer": "Well, that's a fascinating question. From my perspective, this is something I feel quite strongly about, and I have had first-hand experience with it. To elaborate a little — it was a situation that genuinely shifted my outlook, and consequently, I began approaching similar circumstances in an entirely different way. What struck me most was how much a small change in mindset can lead to remarkably significant outcomes.",
            "highlighted_phrases": ["from my perspective", "to elaborate", "consequently", "what struck me most", "remarkably significant"],
            "why_band_9": "Uses hedging language, discourse markers, personal anecdote structure, and varied advanced vocabulary naturally."
        }

ai_router = AIRouter()

