"""
Nano AI v2 - Settings
"""

from pathlib import Path
import os

# ----------------------------
# Project Paths
# ----------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
MEMORY_DIR = ROOT_DIR / "memory"
LOG_DIR = ROOT_DIR / "logs"

for folder in [DATA_DIR, MEMORY_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ----------------------------
# AI Providers
# ----------------------------

DEFAULT_PROVIDER = "ollama"

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ----------------------------
# Voice
# ----------------------------

VOICE_ENABLED = True

WHISPER_MODEL = "small"

TTS_ENGINE = "edge"

VOICE_NAME = "en-US-AvaNeural"

# ----------------------------
# Memory
# ----------------------------

MAX_HISTORY = 20

ENABLE_LONG_TERM_MEMORY = True

# ----------------------------
# Dashboard
# ----------------------------

API_HOST = "127.0.0.1"

API_PORT = 8000

# ----------------------------
# Debug
# ----------------------------

DEBUG = True