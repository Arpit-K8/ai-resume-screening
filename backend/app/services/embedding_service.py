# app/services/embedding_service.py

from google import genai
from app.config import GEMINI_API_KEY, EMBEDDING_MODEL

# We no longer configure globally
if not GEMINI_API_KEY:
    print("Warning: Gemini API key not found.")

def get_embedding(text: str):
    """
    Convert text into embedding vector
    """
    if not GEMINI_API_KEY:
        print("Warning: Gemini client not initialized. Missing API key.")
        return None
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config={"task_type": "RETRIEVAL_DOCUMENT"}
        )
        return result.embeddings[0].values

    except Exception as e:
        print(f"Embedding error: {e}")
        return None


def cosine_similarity(vec1, vec2):
    """
    Compute similarity between two vectors
    """
    import numpy as np

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def compare_texts(text1: str, text2: str):
    """
    Compare two texts using embeddings
    """
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)

    if emb1 is None or emb2 is None:
        return 0

    return cosine_similarity(emb1, emb2)