def generate_report(parsed, score, analysis, decision):
    skills_list = "\n".join([f"- {skill}" for skill in analysis.get('missing_skills', [])])
    risks_list = "\n".join([f"- {risk}" for risk in analysis.get('risk_flags', [])])
    parsed_skills = ", ".join(parsed.get('skills', []))
    experience = parsed.get('experience', 'N/A')
    
    return f"""
### :material/person: Candidate Overview
**Extracted Skills:** {parsed_skills}  
**Experience Level:** {experience}

---

---

### :material/analytics: Compatibility Analysis
**Overall Match Score:** `{score}/100`  
**System Recommendation:** **{decision}**

---

### :material/build: Missing Requirements
{skills_list if skills_list else "- None identified"}

### :material/warning: Potential Risks
{risks_list if risks_list else "- No significant risks identified"}
"""
