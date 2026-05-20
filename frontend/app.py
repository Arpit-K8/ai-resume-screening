import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analyze")

st.set_page_config(page_title="AI Resume Dashboard", layout="wide")

if "started" not in st.session_state:
    st.session_state.started = st.query_params.get("started", "0") == "1"


def render_landing_page() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Manrope:wght@400;600;700&display=swap');

            :root {
                --brand-1: #0a0f2c;
                --brand-2: #112860;
                --accent: #ffd166;
                --card: rgba(255, 255, 255, 0.16);
                --text-main: #f8fbff;
                --text-soft: #d8e4ff;
            }

            .stApp {
                background: radial-gradient(circle at 20% 20%, #1f3f8c 0%, #10224f 38%, #070b1f 100%);
            }

            .hero-wrap {
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 24px;
                background: linear-gradient(145deg, rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0.06));
                backdrop-filter: blur(8px);
                padding: 2.5rem 2rem;
                margin-top: 1rem;
            }

            .hero-inner {
                max-width: 96%;
            }

            .logo-wrap {
                display: flex;
                align-items: center;
                gap: 0.9rem;
                margin-top: 0.4rem;
            }

            .logo-icon {
                width: 54px;
                height: 54px;
                border-radius: 14px;
                background: linear-gradient(135deg, #ffd166, #ff9f1c);
                color: #13204a;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700;
                font-size: 1.05rem;
                box-shadow: 0 8px 30px rgba(255, 209, 102, 0.35);
            }

            .logo-text {
                color: var(--text-main);
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.15rem;
                letter-spacing: 0.02em;
            }

            .logo-sub {
                color: var(--text-soft);
                font-family: 'Manrope', sans-serif;
                font-size: 0.88rem;
            }

            .tag {
                color: #0e1f4a;
                background: var(--accent);
                border-radius: 999px;
                display: inline-block;
                padding: 0.35rem 0.8rem;
                font-family: 'Manrope', sans-serif;
                font-weight: 700;
                font-size: 0.8rem;
                letter-spacing: 0.03em;
            }

            .hero-title {
                font-family: 'Space Grotesk', sans-serif;
                color: var(--text-main);
                font-size: 2.6rem;
                line-height: 1.1;
                margin: 0.8rem 0 0.8rem;
            }

            .hero-sub {
                font-family: 'Manrope', sans-serif;
                color: var(--text-soft);
                font-size: 1.05rem;
                max-width: 58rem;
                margin-bottom: 1.3rem;
            }

            .hero-chip-row {
                display: flex;
                gap: 0.55rem;
                flex-wrap: wrap;
                margin: 1rem 0 0.2rem;
            }

            .hero-chip {
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: #eef5ff;
                border-radius: 999px;
                font-family: 'Manrope', sans-serif;
                font-size: 0.82rem;
                padding: 0.3rem 0.7rem;
                background: rgba(255, 255, 255, 0.1);
            }

            .cta-row {
                display: flex;
                justify-content: flex-start;
                margin-top: 1rem;
            }

            .cta-row [data-testid="stButton"] > button,
            .cta-row div.stButton > button {
                width: auto;
                min-width: 165px;
                padding: 0.7rem 1.2rem;
                border-radius: 999px;
                border: 1px solid rgba(59, 130, 246, 0.55) !important;
                background: linear-gradient(135deg, #60a5fa 0%, #2563eb 50%, #1d4ed8 100%) !important;
                background-color: #2563eb !important;
                color: #f8fbff !important;
                font-weight: 700;
                font-family: 'Manrope', sans-serif;
                box-shadow: 0 12px 30px rgba(37, 99, 235, 0.32) !important;
                transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
                outline: none !important;
                appearance: none !important;
            }

            .cta-row [data-testid="stButton"] > button:hover,
            .cta-row div.stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 16px 36px rgba(37, 99, 235, 0.42) !important;
                filter: brightness(1.03);
                border-color: rgba(96, 165, 250, 0.9) !important;
            }

            .cta-row [data-testid="stButton"] > button:focus,
            .cta-row div.stButton > button:focus {
                outline: none !important;
                box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.2), 0 16px 36px rgba(37, 99, 235, 0.42) !important;
            }

            .right-hero-card {
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 24px;
                min-height: 420px;
                position: relative;
                overflow: hidden;
                background-image:
                    linear-gradient(to top, rgba(7, 15, 40, 0.85), rgba(7, 15, 40, 0.1) 55%),
                    url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80');
                background-size: cover;
                background-position: center;
                box-shadow: 0 20px 55px rgba(0, 0, 0, 0.35);
            }

            .right-hero-badge {
                position: absolute;
                top: 14px;
                right: 14px;
                background: rgba(255, 209, 102, 0.95);
                color: #16214d;
                border-radius: 999px;
                padding: 0.28rem 0.7rem;
                font-family: 'Manrope', sans-serif;
                font-size: 0.78rem;
                font-weight: 700;
            }

            .right-hero-footer {
                position: absolute;
                left: 16px;
                right: 16px;
                bottom: 16px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 14px;
                background: rgba(10, 20, 50, 0.62);
                color: #f1f6ff;
                font-family: 'Manrope', sans-serif;
                padding: 0.8rem 0.95rem;
            }

            .right-hero-footer strong {
                display: block;
                font-size: 0.98rem;
                margin-bottom: 0.12rem;
            }

            .card {
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 18px;
                background: var(--card);
                padding: 1rem 1.1rem;
                height: 100%;
            }

            .card h4 {
                color: var(--text-main);
                font-family: 'Space Grotesk', sans-serif;
                margin-bottom: 0.3rem;
            }

            .card p {
                color: var(--text-soft);
                font-family: 'Manrope', sans-serif;
                margin: 0;
            }

            .step-box {
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 0.8rem 1rem;
                margin-bottom: 0.6rem;
                color: var(--text-soft);
                font-family: 'Manrope', sans-serif;
                background: rgba(255, 255, 255, 0.08);
            }

            @media (max-width: 768px) {
                .hero-title {
                    font-size: 2rem;
                }

                .hero-wrap {
                    padding: 1.4rem 1rem;
                }

                .right-hero-card {
                    min-height: 300px;
                    margin-top: 0.8rem;
                }

                .cta-row [data-testid="stButton"] > button,
                .cta-row div.stButton > button {
                    width: 100%;
                    min-width: 0;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.25, 0.95], gap="large")

    with left_col:
        st.markdown(
            """
            <section class="logo-wrap">
                <div class="logo-icon">ARS</div>
                <div>
                    <div class="logo-text">AI Resume Screening</div>
                    <div class="logo-sub">Fast, free and smart candidate screening</div>
                </div>
            </section>

            <section class="hero-wrap">
                <div class="hero-inner">
                    <span class="tag">AI Resume Screening Platform</span>
                    <h1 class="hero-title">Screen smarter, faster, and with consistent hiring decisions.</h1>
                    <p class="hero-sub">
                        This is a free resume screening platform where you can check candidate fit instantly.
                        No sign up, no login, and no logout required. Upload the resume, paste the job description,
                        and get score, decision, missing skills, and risk insights in one clean report.
                    </p>
                    <div class="hero-chip-row">
                        <span class="hero-chip">100% Free to Use</span>
                        <span class="hero-chip">No Login Needed</span>
                        <span class="hero-chip">Instant AI Report</span>
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        st.markdown(
            """
            <section class="right-hero-card">
                <div class="right-hero-badge">Premium Workflow</div>
                <div class="right-hero-footer">
                    <strong>Designed for quick HR shortlisting</strong>
                    Upload PDF resume and compare against JD with explainable AI decisions.
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="card">
                <h4>What it does</h4>
                <p>Automates resume parsing, fit scoring, and candidate risk analysis from a single PDF + JD input.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
                <h4>Why it helps</h4>
                <p>Reduces manual shortlisting time and keeps evaluation criteria consistent across applicants.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="card">
                <h4>Output you get</h4>
                <p>Match score, hire recommendation, missing skills, risk flags, and a complete explainable report.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader(":material/route: How it works")
    st.markdown('<div class="step-box">1) Upload candidate resume (PDF)</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box">2) Paste the target job description</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box">3) Run analysis to get final recommendation</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="cta-row">', unsafe_allow_html=True)
    if st.button("Get Started", icon=":material/arrow_forward:", type="secondary"):
        st.session_state.started = True
        st.query_params["started"] = "1"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard() -> None:
    # Sidebar
    st.sidebar.title(":material/settings: Input Panel")
    uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd = st.sidebar.text_area("Paste Job Description")

    # Note: `icon` uses streamlit icon token strings
    analyze_btn = st.sidebar.button("Analyze", icon=":material/rocket_launch:")

    st.sidebar.divider()
    if st.sidebar.button("Back to Welcome Page", icon=":material/home:", use_container_width=True):
        st.session_state.started = False
        st.query_params.clear()
        st.rerun()

    # Header
    st.title(":material/dashboard: AI Resume Screening Dashboard")
    st.markdown("### :material/psychology: Smart Hiring Assistant")
    st.markdown("Analyze candidate-job fit using AI agents")

    # Main Area
    if analyze_btn:
        if uploaded_file is not None and jd.strip() != "":
            with st.spinner("Analyzing Resume..."):
                try:
                    # Send proper multipart/form-data with filename and content-type
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"jd": jd}

                    response = requests.post(API_URL, files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()

                        if "error" in result:
                            st.error(result["error"], icon=":material/error:")
                        else:
                            report = result["report"]
                            score = result["score"]
                            decision = result["decision"]
                            skills = result["missing_skills"]
                            risks = result["risks"]

                            st.success("Analysis Complete", icon=":material/check_circle:")

                            if int(score) > 75:
                                st.success("Strong Candidate", icon=":material/thumb_up:")
                            elif int(score) > 50:
                                st.warning("Average Candidate", icon=":material/remove:")
                            else:
                                st.error("Weak Candidate", icon=":material/thumb_down:")

                            # Top Metrics
                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric(":material/monitoring: Match Score", str(score))

                            with col2:
                                st.metric(":material/gavel: Decision", decision)

                            st.divider()

                            # Details Section
                            col3, col4 = st.columns(2)

                            with col3:
                                st.subheader(":material/build: Missing Skills")
                                st.info(", ".join(skills) if skills else "None", icon=":material/info:")

                            with col4:
                                st.subheader(":material/warning: Risk Flags")
                                st.warning(", ".join(risks) if risks else "None", icon=":material/warning:")

                            st.divider()

                            # Full Report
                            st.subheader(":material/description: Full AI Report")
                            with st.container(border=True):
                                st.markdown(report)

                    else:
                        st.error("Backend Error", icon=":material/error:")

                except Exception as e:
                    st.error(f"Error: {e}", icon=":material/error:")

        else:
            st.warning("Upload resume + enter job description", icon=":material/upload_file:")

    else:
        st.info("Upload resume and click Analyze to begin", icon=":material/arrow_back:")


if st.session_state.started:
    render_dashboard()
else:
    render_landing_page()
