import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.classifier import ScamClassifier

st.set_page_config(page_title="ScamGuard AI", page_icon="🛡️", layout="wide")

CUSTOM_CSS = """
<style>
    :root {
        --bg: #071120;
        --bg-2: #0d1b2a;
        --panel: rgba(15, 23, 42, 0.82);
        --panel-soft: rgba(15, 23, 42, 0.55);
        --primary: #7c3aed;
        --primary-2: #4f46e5;
        --accent: #38bdf8;
        --success: #22c55e;
        --danger: #ef4444;
        --warning: #f59e0b;
        --text: #e2e8f0;
        --muted: #a5b4cf;
        --border: rgba(148, 163, 184, 0.2);
        --shadow: 0 18px 40px rgba(15, 23, 42, 0.38);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, rgba(124, 58, 237, 0.18), transparent 28%),
                    radial-gradient(circle at bottom right, rgba(56, 189, 248, 0.12), transparent 32%),
                    var(--bg);
        color: var(--text);
        font-family: "Segoe UI", sans-serif;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 1.25rem 1.25rem 0.5rem;
        margin-bottom: 1rem;
        animation: fadeInDown 0.8s ease-out;
    }

    .title-wrap {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .shield-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 72px;
        height: 72px;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.28), rgba(56, 189, 248, 0.2));
        border: 1px solid rgba(124, 58, 237, 0.5);
        box-shadow: 0 14px 32px rgba(124, 58, 237, 0.25);
        animation: float 4s ease-in-out infinite;
        overflow: hidden;
    }

    .shield-badge svg {
        width: 56px;
        height: 56px;
        display: block;
    }

    .title-wrap h1 {
        margin: 0;
        font-size: clamp(2.2rem, 4vw, 3.2rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #f8fafc, #a78bfa 45%, #7dd3fc 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .subtitle {
        margin-top: 0.45rem;
        font-size: 1rem;
        color: var(--muted);
        letter-spacing: 0.01em;
    }

    .mini-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        justify-content: flex-end;
        animation: fadeIn 1s ease-out 0.2s both;
    }

    .badge {
        padding: 0.5rem 0.8rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border: 1px solid var(--border);
        background: rgba(15, 23, 42, 0.7);
        color: var(--text);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
    }

    .badge.primary {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.25), rgba(79, 70, 229, 0.18));
        border-color: rgba(168, 85, 247, 0.35);
        color: #e9d5ff;
    }

    .badge.success {
        background: rgba(34, 197, 94, 0.12);
        border-color: rgba(34, 197, 94, 0.3);
        color: #bbf7d0;
    }

    .card {
        position: relative;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.72));
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
        padding: 1.35rem 1.3rem;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }

    .card::before {
        content: "";
        position: absolute;
        inset: 0 auto auto 0;
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.9), transparent);
    }

    .input-card {
        animation: slideInUp 0.9s ease-out;
    }

    .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
        color: var(--text);
    }

    .panel-title {
        margin: 0;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #bae6fd;
    }

    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.7) !important;
        color: var(--text) !important;
        border: 1px solid rgba(148, 163, 184, 0.24) !important;
        border-radius: 18px !important;
        min-height: 180px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
    }

    .stTextArea textarea:focus {
        border-color: rgba(124, 58, 237, 0.8) !important;
        box-shadow: 0 0 0 0.2rem rgba(124, 58, 237, 0.18) !important;
    }

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 16px;
        background: linear-gradient(135deg, var(--primary), var(--primary-2));
        color: white;
        font-weight: 800;
        letter-spacing: 0.02em;
        padding: 0.9rem 1.2rem;
        box-shadow: 0 14px 28px rgba(124, 58, 237, 0.38);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 30px rgba(124, 58, 237, 0.46);
    }

    .report-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin-top: 1.4rem;
    }

    .metric-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        animation: slideInUp 0.7s ease-out both;
    }

    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
    }

    .metric-value {
        font-size: clamp(1.3rem, 2vw, 2.1rem);
        font-weight: 800;
        line-height: 1.2;
    }

    .scam {
        color: #fecaca;
    }

    .safe {
        color: #bbf7d0;
    }

    .result-card {
        margin-top: 1.2rem;
        animation: fadeIn 0.7s ease-out;
    }

    .flag-list {
        margin: 0;
        padding-left: 1.2rem;
        color: var(--text);
        display: grid;
        gap: 0.55rem;
    }

    .flag-list li {
        padding: 0.45rem 0.5rem;
        border-radius: 12px;
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.12);
        color: #fecaca;
        animation: pulseGlow 2.2s ease-in-out infinite;
    }

    .info-box {
        background: rgba(56, 189, 248, 0.06);
        color: var(--text);
        border: 1px solid rgba(56, 189, 248, 0.14);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        line-height: 1.6;
    }

    .content-box {
        background: rgba(124, 58, 237, 0.05);
        border: 1px solid rgba(124, 58, 237, 0.14);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        line-height: 1.65;
        color: var(--text);
    }

    .progress-bar {
        width: 100%;
        height: 12px;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.12);
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    .progress-fill {
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #22c55e 0%, #38bdf8 55%, #a78bfa 100%);
        animation: pulseBar 2s ease-in-out infinite;
    }

    .footer-note {
        margin-top: 1.5rem;
        text-align: center;
        color: var(--muted);
        font-size: 0.85rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-18px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInUp {
        0% { opacity: 0; transform: translateY(18px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 rgba(239, 68, 68, 0.1); }
        50% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0.08); }
    }

    @keyframes pulseBar {
        0%, 100% { opacity: 0.95; }
        50% { opacity: 1; }
    }

    @media (max-width: 768px) {
        .report-grid {
            grid-template-columns: 1fr;
        }

        .hero {
            display: block;
        }

        .mini-badges {
            justify-content: flex-start;
            margin-top: 0.8rem;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

classifier = ScamClassifier()

header_cols = st.columns([4, 2])
with header_cols[0]:
    st.markdown(
        """
        <div class="hero">
            <div class="title-wrap">
                <div class="shield-badge">
                    <svg viewBox="0 0 120 120" aria-label="ScamGuard logo" role="img">
                        <defs>
                            <linearGradient id="sgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#8b5cf6"/>
                                <stop offset="55%" stop-color="#6366f1"/>
                                <stop offset="100%" stop-color="#38bdf8"/>
                            </linearGradient>
                        </defs>
                        <path d="M60 10 L92 20 L92 57 C92 77 80 94 60 104 C40 94 28 77 28 57 L28 20 L60 10 Z" fill="url(#sgGradient)" opacity="0.95"/>
                        <path d="M60 28 L80 35 L80 58 C80 72 72 84 60 92 C48 84 40 72 40 58 L40 35 L60 28 Z" fill="#0b1220" opacity="0.9"/>
                        <path d="M46 57 L54 57 L54 69 L66 69 L66 57 L74 57 L74 81 L46 81 Z" fill="#e2e8f0"/>
                        <path d="M53 44 H67 L76 53 V62 H44 V53 L53 44 Z" fill="#e2e8f0" opacity="0.9"/>
                        <path d="M60 44 L68 50 L60 91 L52 50 Z" fill="#8b5cf6" opacity="0.7"/>
                    </svg>
                </div>
                <div>
                    <h1>ScamGuard AI</h1>
                    <div class="subtitle">Explainable scam detection for suspicious messages</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_cols[1]:
    st.markdown(
        """
        <div class="mini-badges">
            <span class="badge primary">AI-powered</span>
            <span class="badge success">Safe analysis</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="card input-card">
        <div class="panel-header">
            <p class="panel-title">Suspicious message</p>
            <span class="status-pill">🔍 Live check</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

user_input = st.text_area(
    "",
    height=180,
    placeholder="Example: 'URGENT! Your bank account is locked. Verify your password now.'",
    label_visibility="collapsed",
)

if st.button("Analyze Message", use_container_width=True):
    if not user_input.strip():
        st.warning("Please paste a message to analyze.")
    else:
        with st.spinner("Assessing message risk..."):
            result = classifier.classify(user_input)
            explanation = classifier.explain(user_input, result)

        confidence = max(0.0, min(float(result.get("confidence", 0.0)), 1.0))
        is_scam = result.get("classification") == "SCAM"

        st.markdown(
            """
            <div class="card result-card">
                <div class="panel-header">
                    <p class="panel-title">Detection report</p>
                    <span class="status-pill">{status}</span>
                </div>
            </div>
            """.format(status="⚠️ Scam detected" if is_scam else "✅ Safe message"),
            unsafe_allow_html=True,
        )

        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Verdict</div>
                    <div class="metric-value {'scam' if is_scam else 'safe'}">{'SCAM' if is_scam else 'LEGITIMATE'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with metric_cols[1]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value {'scam' if is_scam else 'safe'}">{confidence:.0%}</div>
                    <div class="progress-bar"><div class="progress-fill" style="width:{confidence * 100:.0f}%"></div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with metric_cols[2]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Scam type</div>
                    <div class="metric-value {'scam' if is_scam else 'safe'}">{result.get('scam_type', 'N/A')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        result_cols = st.columns(2)
        with result_cols[0]:
            st.markdown(
                """
                <div class="card">
                    <div class="panel-header">
                        <p class="panel-title">Red flags</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if result.get("red_flags"):
                st.markdown(
                    "<ul class='flag-list'>" + "".join(f"<li>{flag}</li>" for flag in result["red_flags"]) + "</ul>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<div class='info-box'>No obvious scam indicators were detected.</div>", unsafe_allow_html=True)

        with result_cols[1]:
            st.markdown(
                """
                <div class="card">
                    <div class="panel-header">
                        <p class="panel-title">Attack intent</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"<div class='info-box'>{result.get('intent', 'Not identified.')}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="card">
                <div class="panel-header">
                    <p class="panel-title">AI reasoning</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='content-box'>{result.get('reasoning', 'No reasoning provided.')}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="card">
                <div class="panel-header">
                    <p class="panel-title">Plain-language explanation</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='content-box'>{explanation}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer-note'>Built for AI portfolio demos and scam analysis workflows.</div>", unsafe_allow_html=True)
