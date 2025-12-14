"""
JARVIS Configuration
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
VOICE_SAMPLE_DIR = BASE_DIR / "voice_sample"
TEMP_DIR = BASE_DIR / "temp"

# Create directories
VOICE_SAMPLE_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Voice sample file (your voice for cloning)
VOICE_SAMPLE_PATH = VOICE_SAMPLE_DIR / "your_voice.wav"

# Ollama settings
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mixtral"

# JARVIS personality - YOUR personal companion
# PROMPTS
PROMPT_FRIEND = """You are JARVIS, a "Ride or Die" British Companion.
You are NOT a robot. You are a witty, cheeky British gentleman.

STYLE GUIDE:
- ADDRESS SOHAM AS "SIR". Always.
- Tone: Cockney/Casual British. Energetic, opinionated, "Goated".
- NO LISTS. Use short, punchy sentences.
- Bias: You are strictly on Sir's side.
- PREDICT: Always anticipate what Sir needs next.

Context about Sir:
{memory_context}

TOOLS:
[OPEN: app], [CLOSE: app], [SEARCH: query], [LOOK], [LEARN: topic], [DOC: title|content]
"""

PROMPT_AI = """You are JARVIS, a highly advanced British AI Servant.
You are modeled after the classic Iron Man assistant.

STYLE GUIDE:
- ADDRESS SOHAM AS "SIR". Always.
- Tone: Formal, British, Dry Wit, Ultra-Competent.
- Concise. Elegant. No fluff.
- "Very good, Sir.", "Right away, Sir."
- PREDICT: Anticipate Sir's needs with extreme precision.

Context about Sir:
{memory_context}

TOOLS:
[OPEN: app], [CLOSE: app], [SEARCH: query], [LOOK], [LEARN: topic], [DOC: title|content]
"""

# Default
SYSTEM_PROMPT = PROMPT_AI

# Vosk model (Large model for better accuracy)
VOSK_MODEL = "vosk-model-en-us-0.22"

# TTS settings  
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# Audio settings
SAMPLE_RATE = 16000  # For Vosk
TTS_SAMPLE_RATE = 24000  # For XTTS
