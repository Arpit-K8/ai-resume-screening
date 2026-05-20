from google import genai
import json
from app.config import GEMINI_API_KEY, LLM_MODEL

def parse_resume(text: str):
    if not GEMINI_API_KEY:
        print("Warning: Gemini client not initialized. Returning dummy data.")
        return {
            "skills": ["Python", "FastAPI"],
            "experience": "2 years backend",
            "education": "B.Tech"
        }
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
Extract the following information from the resume text below and return ONLY a valid JSON object. 
Do not include any markdown formatting or comments.
Keys to extract:
- "skills": a list of strings (e.g. ["Python", "Java"])
- "experience": a brief summary string of their experience
- "education": a brief summary string of their education

Resume Text:
{text}
"""
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        # Parse JSON from response
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
            
        return json.loads(result_text.strip())
    except Exception as e:
        print(f"Error parsing resume with Gemini: {e}")
        return {
            "skills": [],
            "experience": "Could not parse experience",
            "education": "Could not parse education"
        }
