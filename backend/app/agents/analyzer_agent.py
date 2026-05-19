from google import genai
import json
from app.config import GEMINI_API_KEY, LLM_MODEL

def analyze_gaps(parsed_data, jd):
    if not GEMINI_API_KEY:
        print("Warning: Gemini client not initialized. Returning dummy data.")
        return {
            "missing_skills": ["(Pending AI Analysis - Replace with LLM logic)"],
            "risk_flags": ["(Pending AI Analysis - Replace with LLM logic)"]
        }
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
Compare the parsed resume data with the job description. Identify missing skills and any risk flags.
Return ONLY a valid JSON object. Do not include markdown formatting or comments.
Keys to extract:
- "missing_skills": a list of strings
- "risk_flags": a list of strings

Parsed Resume Data:
{json.dumps(parsed_data)}

Job Description:
{jd}
"""
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        # Parse JSON
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
            
        return json.loads(result_text.strip())
    except Exception as e:
        print(f"Error analyzing gaps with Gemini: {e}")
        return {
            "error": f"Error analyzing with AI: {str(e)}",
            "missing_skills": [f"Error analyzing with AI: {str(e)}"],
            "risk_flags": [f"Error analyzing with AI: {str(e)}"]
        }
