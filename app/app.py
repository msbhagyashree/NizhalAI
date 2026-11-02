
import sys
from pathlib import Path

import streamlit as st


# --------------------------------------------------
# PROJECT CONNECTION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agent.app import run


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NizhalAI | Climate Safety",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# --------------------------------------------------
# MADURAI KOLAM THEME
# --------------------------------------------------

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Kavivanar&family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>

:root {
    --kavi: #8B2635;
    --rice: #F9F6F0;
    --parrot: #2E8B57;
    --marigold: #FF8C00;
    --ink: #302B29;
    --muted: #625B55;
}

.stApp {
    background-color: var(--rice);
    font-family: 'Inter', 'Noto Sans Tamil', sans-serif;
    color: var(--ink);
}

[data-testid="stMain"] {
    background-color: var(--rice);
}

[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] li {
    color: var(--ink);
    line-height: 1.8;
}

h1, h2, h3 {
    color: var(--kavi) !important;
    font-family: 'Inter', 'Kavivanar', sans-serif !important;
    line-height: 1.6 !important;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #29262D;
}

[data-testid="stSidebar"] * {
    color: #F9F6F0;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F9F6F0 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #62565A;
    margin-top: 25px;
    margin-bottom: 25px;
}

/* Feature cards */

.kolam-card {
    position: relative;
    background-color: #FFFFFF;
    border: 1px solid #E5D9CC;
    border-radius: 16px;
    padding: 24px 20px;
    min-height: 150px;
    margin-bottom: 14px;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(60, 35, 30, 0.04);
    background-image: radial-gradient(#D8C9B9 0.7px, transparent 0.7px);
    background-size: 17px 17px;
}

.kolam-card:before {
    content: "";
    position: absolute;
    top: 8px;
    right: 8px;
    width: 25px;
    height: 25px;
    border-top: 2px solid var(--marigold);
    border-right: 2px solid var(--marigold);
    border-radius: 0 8px 0 0;
}

.kolam-card h3 {
    color: var(--kavi);
    font-size: 21px;
    margin-top: 0;
    margin-bottom: 12px;
}

.kolam-card p {
    color: var(--ink);
    font-size: 15px;
    margin-bottom: 0;
}

/* Buttons */

.stButton > button {
    background-color: var(--kavi);
    color: white !important;
    border: 1px solid var(--kavi);
    border-radius: 10px;
    padding: 9px 18px;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background-color: #6F1C2A;
    border-color: var(--marigold);
    color: white !important;
    box-shadow: 0 4px 12px rgba(139, 38, 53, 0.2);
}

/* Input fields */

.stTextInput input,
.stTextArea textarea,
[data-testid="stChatInput"] textarea {
    background-color: white !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    border: 1px solid #D7C9BC !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #625B55 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #625B55 !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: white;
    border-radius: 9px;
}

/* Chat messages */

[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid #E9DED3;
    border-radius: 14px;
    padding: 14px;
}


/* Fix visibility of all assistant response text */
[data-testid="stChatMessage"],
[data-testid="stChatMessage"] .stMarkdown,
[data-testid="stChatMessage"] .stMarkdown p,
[data-testid="stChatMessage"] .stMarkdown li,
[data-testid="stChatMessage"] .stMarkdown ol,
[data-testid="stChatMessage"] .stMarkdown ul,
[data-testid="stChatMessage"] .stMarkdown strong {
    color: #302B29 !important;
    opacity: 1 !important;
}

[data-testid="stChatMessage"] .stMarkdown p,
[data-testid="stChatMessage"] .stMarkdown li {
    line-height: 1.9 !important;
}

[data-testid="stChatMessage"] .stMarkdown li::marker {
    color: #8B2635 !important;
}

[data-testid="stChatInput"] {
    background-color: var(--rice);
}

/* Alerts and citations */


/* Emergency and warning message visibility */
[data-testid="stAlert"] {
    border-radius: 12px;
    background-color: #FFF4B8 !important;
    border: 1px solid #E5B94C !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #302B29 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #302B29 !important;
}

[data-testid="stAlert"] svg {
    color: #8B2635 !important;
    fill: #8B2635 !important;
}

.citation-text {
    color: var(--parrot);
    font-size: 13px;
    font-weight: 600;
}

/* Subtitle */

.subtitle {
    color: var(--muted);
    font-size: 17px;
    line-height: 1.8;
}

/* Kolam divider */

.kolam-divider {
    height: 3px;
    background: linear-gradient(
        90deg,
        var(--kavi),
        var(--marigold),
        var(--parrot),
        transparent
    );
    border-radius: 5px;
    margin: 24px 0;
}

/* Loading animation */

.kolam-loader {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px;
    color: var(--kavi);
    font-weight: 600;
}

.kolam-loader svg {
    width: 48px;
    height: 48px;
    animation: kolam-spin 5s linear infinite;
}

.kolam-loader circle {
    fill: none;
    stroke: var(--kavi);
    stroke-width: 2.5;
    stroke-dasharray: 4 3;
}

.kolam-loader .kolam-inner {
    stroke: var(--marigold);
}

@keyframes kolam-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
    .kolam-loader svg {
        animation: none;
    }

    .stButton > button {
        transition: none;
    }
}

/* Footer */

.footer-text {
    text-align: center;
    color: var(--muted);
    font-size: 13px;
    padding: 25px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        "<h2>🌿 NizhalAI</h2>",
        unsafe_allow_html=True
    )

    st.caption("Community Climate Safety Assistant")

    st.markdown("---")

    st.markdown("### Choose your language")

    language = st.selectbox(
        "Preferred language",
        ["English", "Tamil"],
        label_visibility="visible"
    )

    st.markdown("---")

    st.markdown("### What can NizhalAI help with?")

    st.markdown("""
    🌡️ Heat-risk estimation

    ☀️ Heat-safety guidance

    💧 Water conservation

    🏡 Community preparedness

    🚨 Emergency guidance
    """)

    st.markdown("---")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.markdown("---")

    st.markdown(
        "<p style='font-size:13px;color:#E8DCD5;'>"
        "Inspired by Madurai's cultural heritage.<br>"
        "Designed for safer, climate-resilient communities."
        "</p>",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    """
    <h1 style="margin-bottom:0;">🌿 NizhalAI</h1>
    <p class="subtitle">
        Building climate-resilient communities through AI.
    </p>
    <div class="kolam-divider"></div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="kolam-card">
        <h3>🌡️ Heat Safety</h3>
        <p>Understand heat exposure and get practical safety advice.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kolam-card">
        <h3>💧 Water Awareness</h3>
        <p>Explore water conservation and rainwater harvesting.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kolam-card">
        <h3>🏡 Community Resilience</h3>
        <p>Prepare vulnerable communities for climate challenges.</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("## 💬 Ask NizhalAI")

st.markdown(
    '<p class="subtitle">Ask a question about heat safety, water stress, or community climate preparedness.</p>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SAMPLE QUESTIONS
# --------------------------------------------------

st.markdown("### Try asking")

if language == "Tamil":

    sample_questions = [
        "வெயிலில் வேலை செய்யும் வியாபாரிகள் தங்களை எப்படிப் பாதுகாக்கலாம்?",
        "தண்ணீரை எவ்வாறு சேமிக்கலாம்?",
        "வெப்ப அழுத்தத்தின் அறிகுறிகள் என்ன?"
    ]

else:

    sample_questions = [
        "How can street vendors protect themselves from extreme heat?",
        "How can communities conserve water?",
        "What are the warning signs of heat stress?"
    ]


sample_columns = st.columns(3)

for index, question in enumerate(sample_questions):

    with sample_columns[index]:

        if st.button(
            question,
            key=f"sample_{index}",
            use_container_width=True
        ):
            st.session_state.pending_question = question
            st.rerun()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if message.get("steps"):
                st.markdown("**Suggested actions**")

                for step in message["steps"]:
                    st.markdown(f"- {step}")

            if message.get("escalation"):
                st.warning(message["escalation"])

            if message.get("citations"):
                st.markdown(
                    "**Guidance references:** "
                    + ", ".join(message["citations"])
                )


# --------------------------------------------------
# PROCESS USER QUESTION
# --------------------------------------------------

prompt = st.chat_input("Type your question here...")

if st.session_state.pending_question:

    prompt = st.session_state.pending_question
    st.session_state.pending_question = None


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        loading_area = st.empty()

        loading_area.markdown("""
        <div class="kolam-loader">
            <svg viewBox="0 0 100 100" aria-label="Loading">
                <circle cx="50" cy="50" r="38"/>
                <circle class="kolam-inner" cx="50" cy="50" r="25"/>
                <circle cx="50" cy="50" r="12"/>
                <path d="M50 12 Q88 50 50 88 Q12 50 50 12"
                      fill="none" stroke="#2E8B57" stroke-width="2.5"/>
                <path d="M12 50 Q50 12 88 50 Q50 88 12 50"
                      fill="none" stroke="#FF8C00" stroke-width="2.5"/>
            </svg>
            <span>NizhalAI is thinking...</span>
        </div>
        """, unsafe_allow_html=True)

        try:

            # Call the actual NizhalAI agent
            response = run({"text": prompt})

            loading_area.empty()

            # IMPORTANT: Extract the nested structured plan
            if isinstance(response, dict):

                plan = response.get("plan", response)

                answer = plan.get("answer", "")
                steps = plan.get("steps", [])
                escalation = plan.get("escalation", "")
                citations = plan.get("citations", [])

            else:

                answer = getattr(response, "answer", "")
                steps = getattr(response, "steps", [])
                escalation = getattr(response, "escalation", "")
                citations = getattr(response, "citations", [])

            # Do not silently display an empty response
            if not answer:
                raise ValueError(
                    "The agent returned an empty answer. "
                    "Please check the response structure."
                )

            # Display answer
            st.markdown(answer)

            if steps:

                st.markdown("**Suggested actions**")

                for step in steps:
                    st.markdown(f"- {step}")

            if escalation:
                st.warning(escalation)

            if citations:

                st.markdown(
                    "**Guidance references:** "
                    + ", ".join(citations)
                )

            # Save complete assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "steps": steps,
                "escalation": escalation,
                "citations": citations
            })

        except Exception as error:

            loading_area.empty()

            st.error(
                "Sorry, NizhalAI could not process your request."
            )

            st.caption(f"Technical details: {error}")

            st.info(
                "Please check your AWS Bedrock connection and try again."
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="kolam-divider"></div>
<div class="footer-text">
    🌿 NizhalAI · Community Climate Safety Assistant<br>
    Inspired by Madurai · Powered by Strands SDK and Amazon Bedrock
</div>
""", unsafe_allow_html=True)
