from app.services.embedding_service import compare_texts

def match_with_jd(parsed_data, jd):
    resume_text = " ".join(parsed_data["skills"]) + " " + parsed_data["experience"]

    score = compare_texts(resume_text, jd)

    return round(score * 100)