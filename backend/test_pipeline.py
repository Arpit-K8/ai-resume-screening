import os
from dotenv import load_dotenv

# Load the .env file from the parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from app.agents.parser_agent import parse_resume
from app.agents.analyzer_agent import analyze_gaps
from app.services.embedding_service import compare_texts

# Mock Resume and JD
resume_text = """
John Doe
Software Engineer
Experience: 3 years working with Python, Django, and PostgreSQL. Built REST APIs and optimized database queries.
Education: B.S. in Computer Science
Skills: Python, Django, SQL, Git, Docker
"""

job_description = """
We are looking for a Backend Python Developer.
Requirements:
- 2+ years of experience with Python and FastAPI.
- Experience with relational databases like PostgreSQL.
- Familiarity with containerization (Docker).
- AWS experience is a big plus.
"""

print("--- Testing Parser Agent ---")
parsed_resume = parse_resume(resume_text)
print("Parsed Resume Data:")
print(parsed_resume)

print("\n--- Testing Analyzer Agent ---")
analysis_results = analyze_gaps(parsed_resume, job_description)
print("Analysis Results:")
print(analysis_results)

print("\n--- Testing Embedding Service ---")
# Create a summarized text for embedding comparison
resume_summary = " ".join(parsed_resume.get("skills", [])) + " " + parsed_resume.get("experience", "")
similarity_score = compare_texts(resume_summary, job_description)
print(f"Similarity Score (Cosine Distance): {similarity_score:.4f}")
