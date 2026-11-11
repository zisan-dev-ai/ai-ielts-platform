# -*- coding: utf-8 -*-
"""
Multi-Speaker IELTS Neural Audio Synthesis Engine.
Generates authentic Cambridge-quality audio where multiple speakers (dialogues,
tutor-student discussions, interviews) have completely distinct, realistic voices.
"""

import os
import re
import asyncio
import hashlib
import tempfile
import requests
from typing import List, Tuple, Dict, Any, Optional

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


# Curated Authentic British, Australian & Academic Neural Voices
VOICE_CATALOG = {
    # British Voices
    "gb_female_mature": "en-GB-SoniaNeural",
    "gb_male_mature": "en-GB-RyanNeural",
    "gb_female_young": "en-GB-LibbyNeural",
    "gb_male_academic": "en-GB-ThomasNeural",
    "gb_female_lively": "en-GB-MaisieNeural",
    
    # Australian Voices (Common in IELTS)
    "au_female": "en-AU-NatashaNeural",
    "au_male": "en-AU-WilliamMultilingualNeural",
    
    # North American Voices (Occasional IELTS international speakers)
    "ca_male": "en-CA-LiamNeural",
    "ca_female": "en-CA-ClaraNeural",
    "us_male": "en-US-GuyNeural",
    "us_female": "en-US-JennyNeural"
}

# Persona Voice Map for common IELTS roles
PERSONA_VOICE_RULES = {
    # Females
    "chloe": "en-GB-LibbyNeural",
    "maya": "en-AU-NatashaNeural",
    "sarah": "en-GB-SoniaNeural",
    "rachel": "en-CA-ClaraNeural",
    "clara": "en-CA-ClaraNeural",
    "jenny": "en-US-JennyNeural",
    "anna": "en-GB-LibbyNeural",
    "emma": "en-AU-NatashaNeural",
    "lucy": "en-GB-MaisieNeural",
    "customer_female": "en-GB-SoniaNeural",
    "caller_female": "en-AU-NatashaNeural",
    "student_female": "en-GB-LibbyNeural",

    # Males
    "liam": "en-CA-LiamNeural",
    "jack": "en-AU-WilliamMultilingualNeural",
    "leo": "en-GB-RyanNeural",
    "mark": "en-GB-RyanNeural",
    "kenji": "en-AU-WilliamMultilingualNeural",
    "david": "en-GB-RyanNeural",
    "tom": "en-GB-ThomasNeural",
    "officer": "en-GB-RyanNeural",
    "agent": "en-GB-RyanNeural",
    "ranger": "en-AU-WilliamMultilingualNeural",
    "coordinator": "en-GB-RyanNeural",
    "guide": "en-GB-RyanNeural",
    "lecturer": "en-GB-ThomasNeural",
    "professor": "en-GB-ThomasNeural",
    "dr_evans": "en-GB-ThomasNeural",
    "tutor": "en-GB-ThomasNeural",
}

DEFAULT_VOICE_ROTATION = [
    "en-GB-RyanNeural",           # Male 1
    "en-GB-SoniaNeural",          # Female 1
    "en-AU-WilliamMultilingualNeural",  # Male 2
    "en-AU-NatashaNeural",        # Female 2
    "en-GB-ThomasNeural",         # Male 3 (Academic)
    "en-GB-LibbyNeural",          # Female 3 (Young)
]


class MultiSpeakerAudioSynthesizer:
    """
    Parses transcript dialogue turns and synthesizes seamless multi-speaker audio.
    """

    @staticmethod
    def parse_speakers(transcript: str) -> List[Tuple[str, str]]:
        """
        Parses a raw IELTS transcript into a list of (speaker, text) turns.
        """
        lines = [l.strip() for l in transcript.split("\n") if l.strip()]
        turns = []
        current_speaker = "Narrator"
        
        for line in lines:
            if line.startswith("TRANSCRIPT"):
                continue
                
            # Regex to match speaker prefix e.g. "Officer: ...", "Dr Evans: ...", "Liam: ..."
            match = re.match(r'^([A-Za-z0-9\.\s]+?):\s*(.+)$', line)
            if match:
                speaker_tag = match.group(1).strip()
                dialogue_text = match.group(2).strip()
                # Verify it's a genuine speaker tag (not a regular sentence with colon)
                if len(speaker_tag.split()) <= 4 and len(speaker_tag) < 30:
                    current_speaker = speaker_tag
                    turns.append((current_speaker, dialogue_text))
                    continue

            # Continuation of previous speaker
            if turns:
                prev_speaker, prev_text = turns[-1]
                turns[-1] = (prev_speaker, prev_text + " " + line)
            else:
                turns.append((current_speaker, line))

        return turns

    @classmethod
    def assign_voices(cls, turns: List[Tuple[str, str]], section_num: int = 1) -> Dict[str, str]:
        """
        Maps each distinct speaker in the conversation to a unique Neural Voice.
        """
        distinct_speakers = []
        for speaker, _ in turns:
            if speaker not in distinct_speakers:
                distinct_speakers.append(speaker)

        speaker_voice_map = {}
        used_voices = set()
        
        for idx, speaker in enumerate(distinct_speakers):
            s_clean = speaker.lower().replace(".", "").replace(" ", "_")
            
            # 1. Check direct persona rules
            matched_voice = None
            for rule_key, v_name in PERSONA_VOICE_RULES.items():
                if rule_key in s_clean:
                    matched_voice = v_name
                    break
            
            # 2. If no direct rule, pick from default voice rotation
            if not matched_voice or matched_voice in used_voices:
                for candidate in DEFAULT_VOICE_ROTATION:
                    if candidate not in used_voices:
                        matched_voice = candidate
                        break
                if not matched_voice:
                    matched_voice = DEFAULT_VOICE_ROTATION[idx % len(DEFAULT_VOICE_ROTATION)]
            
            speaker_voice_map[speaker] = matched_voice
            used_voices.add(matched_voice)

        return speaker_voice_map

    @classmethod
    async def synthesize_turn_edge(cls, text: str, voice: str) -> bytes:
        """Synthesizes a single dialogue turn using edge-tts"""
        if not text.strip():
            return b""
        com = edge_tts.Communicate(text, voice)
        audio_chunks = []
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
        return b"".join(audio_chunks)

    @classmethod
    def synthesize_turn_gtts_fallback(cls, text: str, lang: str = "en-GB") -> bytes:
        """Fallback to Google TTS with regional accent variations"""
        if not text.strip():
            return b""
        url = f"https://translate.googleapis.com/translate_tts?ie=UTF-8&q={requests.utils.quote(text[:200])}&tl={lang}&client=tw-ob"
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=6)
            if r.status_code == 200:
                return r.content
        except Exception:
            pass
        return b""

    @classmethod
    async def synthesize_transcript(cls, transcript: str, section_num: int = 1) -> bytes:
        """
        Synthesizes a full transcript with multi-speaker distinct voices.
        """
        turns = cls.parse_speakers(transcript)
        if not turns:
            return b""

        speaker_voices = cls.assign_voices(turns, section_num)
        audio_segments = []

        # Process each dialogue turn with its speaker's assigned voice
        for speaker, text in turns:
            voice = speaker_voices.get(speaker, "en-GB-RyanNeural")
            
            # Split long dialogues into manageable sentences to prevent TTS timeouts
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
            if not sentences:
                sentences = [text]

            for sentence in sentences:
                turn_bytes = b""
                if HAS_EDGE_TTS:
                    try:
                        turn_bytes = await cls.synthesize_turn_edge(sentence, voice)
                    except Exception as e:
                        print(f"EdgeTTS error for '{speaker}': {e}, using fallback")
                
                if not turn_bytes or len(turn_bytes) < 100:
                    # Fallback
                    acc = "en-GB" if "GB" in voice else ("en-AU" if "AU" in voice else "en-CA")
                    turn_bytes = cls.synthesize_turn_gtts_fallback(sentence, acc)
                
                if turn_bytes:
                    audio_segments.append(turn_bytes)

        return b"".join(audio_segments)


def generate_multi_speaker_listening_audio(transcript: str, section_num: int = 1) -> bytes:
    """Synchronous entry point for FastAPI endpoints"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        return loop.run_until_complete(MultiSpeakerAudioSynthesizer.synthesize_transcript(transcript, section_num))
    else:
        return loop.run_until_complete(MultiSpeakerAudioSynthesizer.synthesize_transcript(transcript, section_num))
