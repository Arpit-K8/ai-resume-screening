# AI Resume Screening System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-resume-screening-a3ccbtzeevwwbajvcsqff8.streamlit.app/)

**Live Demo:** [AI Resume Screening Dashboard](https://ai-resume-screening-a3ccbtzeevwwbajvcsqff8.streamlit.app/)

An end-to-end hiring assistant that scores how well a candidate’s resume fits a job description. Upload a PDF resume, paste a job description (JD), and the system returns a match score, hire/maybe/reject recommendation, gap analysis, and a structured report—powered by Google Gemini and semantic embeddings.

## Features

- **PDF resume ingestion** — Extracts text from uploaded PDFs via `pdfplumber`
- **Structured resume parsing** — LLM extracts skills, experience summary, and education as JSON
- **Semantic match scoring** — Gemini embeddings + cosine similarity between resume summary and JD
- **Gap & risk analysis** — Identifies missing skills and risk flags compared to the JD
- **Automated decision** — `Hire` / `Maybe` / `Reject` based on configurable score thresholds
- **Recruiter-friendly report** — Markdown report suitable for the Streamlit dashboard
- **Streamlit UI** — Sidebar upload + JD input, metrics, and full report view

## Architecture

The backend runs a linear **multi-agent pipeline** on each `/analyze` request:

```
PDF Upload → PDF Service (text extraction)
          → Parser Agent (Gemini LLM → skills, experience, education)
          → Matcher Agent (embeddings → match score 0–100)
          → Analyzer Agent (Gemini LLM → missing skills, risk flags)
          → Decision Agent (threshold rules → Hire / Maybe / Reject)
          → Report Agent (formatted markdown report)
```

| Agent | Role | Technology |
|-------|------|------------|
| **Parser** | Extract structured fields from raw resume text | Gemini (`LLM_MODEL`) |
| **Matcher** | Score resume–JD fit | Gemini embeddings + cosine similarity |
| **Analyzer** | Compare parsed resume vs JD for gaps and risks | Gemini (`LLM_MODEL`) |
| **Decision** | Map score to recommendation | Rule-based thresholds |
| **Report** | Assemble final markdown output | Template assembly |

> **Note:** `rag_service.py` and `data/knowledge_base.txt` provide a placeholder knowledge base for future RAG enhancements; they are not wired into the main API flow yet.

## Project structure

```
ai-resume-screening/
├── .env                          # GEMINI_API_KEY (do not commit)
├── frontend/
│   └── app.py                    # Streamlit dashboard
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── test_pipeline.py          # End-to-end agent smoke test
    ├── test_gemini.py            # Embedding API sanity check
    ├── data/
    │   └── knowledge_base.txt    # Sample role/skill reference (future RAG)
    └── app/
        ├── main.py               # FastAPI app entry
        ├── config.py             # Models, thresholds, env loading
        ├── api/
        │   └── routes.py         # POST /analyze
        ├── agents/
        │   ├── parser_agent.py
        │   ├── matcher_agent.py
        │   ├── analyzer_agent.py
        │   ├── decision_agent.py
        │   └── report_agent.py
        ├── models/
        │   └── schemas.py
        └── services/
            ├── pdf_service.py
            ├── embedding_service.py
            └── rag_service.py
```

## Tech stack

| Layer | Stack |
|-------|--------|
| API | [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/) |
| UI | [Streamlit](https://streamlit.io/) |
| LLM & embeddings | [Google Gen AI SDK](https://github.com/googleapis/python-genai) (`google-genai`) |
| PDF | [pdfplumber](https://github.com/jsvine/pdfplumber) |
| Vectors | NumPy (cosine similarity) |

## Prerequisites

- **Python 3.10+**
- A **[Google AI / Gemini API key](https://aistudio.google.com/apikey)**

## Setup

### 1. Clone and enter the project

```bash
cd ai-resume-screening
```

### 2. Environment variables

Create a `.env` file in the **project root** (`ai-resume-screening/.env`):

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit real API keys. Add `.env` to `.gitignore` if you use version control.

When running the API from `backend/`, either copy `.env` into `backend/` or export `GEMINI_API_KEY` in your shell so `app/config.py` can load it.

### 3. Install backend dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Streamlit is listed in `requirements.txt`; the same environment can run both backend and frontend.

## Running locally

Use **two terminals**: API first, then the dashboard.

### Terminal 1 — FastAPI backend

From `backend/` (with venv activated):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API root: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

### Terminal 2 — Streamlit frontend

From `frontend/`:

```bash
streamlit run app.py
```

The UI calls `http://127.0.0.1:8000/analyze` by default. Change `API_URL` in `frontend/app.py` if the backend runs elsewhere.

### Workflow

1. Upload a **PDF** resume in the sidebar.
2. Paste the **job description**.
3. Click **Analyze**.
4. Review match score, decision, missing skills, risk flags, and the full AI report.

### Score interpretation (UI & decision logic)

| Match score | UI hint | Decision |
|-------------|---------|----------|
| > 75 | Strong candidate | **Hire** |
| 51–75 | Average candidate | **Maybe** |
| ≤ 50 | Weak candidate | **Reject** |

Thresholds are defined in `backend/app/config.py` (`HIGH_MATCH_THRESHOLD`, `MEDIUM_MATCH_THRESHOLD`). The decision agent currently uses the same 75 / 50 cutoffs inline.

## API reference

### `POST /analyze`

Multipart form request.

| Field | Type | Description |
|-------|------|-------------|
| `file` | PDF file | Candidate resume |
| `jd` | string (form) | Job description text |

**Example response**

```json
{
  "score": 82,
  "decision": "Hire",
  "missing_skills": ["AWS", "FastAPI"],
  "risks": ["Limited cloud experience"],
  "report": "### Candidate Overview\n..."
}
```

| Field | Description |
|-------|-------------|
| `score` | Match score 0–100 (embedding similarity × 100, rounded) |
| `decision` | `Hire`, `Maybe`, or `Reject` |
| `missing_skills` | Skills from JD not adequately covered on resume |
| `risks` | Potential hiring risks flagged by the analyzer |
| `report` | Markdown report for display in Streamlit |

## Configuration

Settings in `backend/app/config.py`:

| Variable | Default | Purpose |
|----------|---------|---------|
| `LLM_MODEL` | `gemini-3-flash-preview` | Parser & analyzer |
| `EMBEDDING_MODEL` | `models/gemini-embedding-2` | Resume–JD similarity |
| `MAX_FILE_SIZE_MB` | `5` | Intended upload limit (enforce in routes if needed) |
| `SIMILARITY_THRESHOLD` | `0.75` | Reference threshold for embeddings |
| `HIGH_MATCH_THRESHOLD` | `75` | Hire boundary |
| `MEDIUM_MATCH_THRESHOLD` | `50` | Maybe boundary |

Without `GEMINI_API_KEY`, parser and analyzer return placeholder data and embedding comparison returns `0`.

## Docker (backend only)

From `backend/`:

```bash
docker build -t ai-resume-screening-api .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_api_key_here ai-resume-screening-api
```

The image starts Uvicorn on port `8000`. Run the Streamlit app separately on the host, or extend the setup with a compose file if you containerize the UI later.

## Testing

From `backend/` with `GEMINI_API_KEY` set (loads `.env` from project root in the test scripts):

```bash
# Parser, analyzer, and embedding pipeline
python test_pipeline.py

# Low-level embedding API check
python test_gemini.py
```

## Development notes

- **Graceful degradation:** Missing API key yields dummy parser/analyzer output and zero similarity scores.
- **JSON responses:** Parser and analyzer request `application/json` from Gemini and strip markdown code fences when present.
- **Security:** Treat resumes and JDs as sensitive data; restrict network access in production and rotate API keys if exposed.
- **Future work:** Integrate `rag_service` with `knowledge_base.txt` for role-specific skill retrieval; align `decision_agent` with `config` thresholds; enforce `MAX_FILE_SIZE_MB` on uploads.

## License

Add a license file if you plan to open-source or distribute this project.
