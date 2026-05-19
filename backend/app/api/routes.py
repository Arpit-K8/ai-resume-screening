from fastapi import APIRouter, UploadFile, File, Form
from app.services.pdf_service import extract_text_from_pdf
from app.agents.parser_agent import parse_resume
from app.agents.matcher_agent import match_with_jd
from app.agents.analyzer_agent import analyze_gaps
from app.agents.decision_agent import make_decision
from app.agents.report_agent import generate_report

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    jd: str = Form(...)
):
    
    resume_text = extract_text_from_pdf(file)

    parsed_data = parse_resume(resume_text)
    match_score = match_with_jd(parsed_data, jd)
    analysis = analyze_gaps(parsed_data, jd)
    
    if "error" in analysis or (analysis.get("missing_skills") and "Error" in str(analysis["missing_skills"][0])):
        return {
            "error": analysis.get("error", "Error processing job description or resume. Please check your inputs.")
        }
        
    decision = make_decision(match_score, analysis)

    report = generate_report(parsed_data, match_score, analysis, decision)

    return {
        "score": match_score,
        "decision": decision,
        "missing_skills": analysis.get("missing_skills", []),
        "risks": analysis.get("risk_flags", []),
        "report": report
    }
