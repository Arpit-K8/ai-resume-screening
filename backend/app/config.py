# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Model configs
LLM_MODEL = "gemini-3-flash-preview"
EMBEDDING_MODEL = "models/gemini-embedding-2"
# App configs
MAX_FILE_SIZE_MB = 5
SIMILARITY_THRESHOLD = 0.75
# Decision thresholds
HIGH_MATCH_THRESHOLD = 75
MEDIUM_MATCH_THRESHOLD = 50