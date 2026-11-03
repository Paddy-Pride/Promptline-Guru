import os
import streamlit as st
from groq import Groq

# ============================================================
# Craftline
# From rough idea to professional prompt.
# Groq API only. Voice input via Groq Whisper.
# ============================================================

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="Craftline",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #000000; font-weight: 700; letter-spacing: -0.02em; }
    h1 { font-size: 2.2rem; border-bottom: 4px solid #FFCC00; padding-bottom: 0.4rem; display: inline-block; }
    .stButton > button { background-color: #FFCC00; color: #000000; border: 2px solid #000000; border-radius: 30px; font-weight: 700; padding: 0.6rem 1.8rem; font-size: 0.95rem; transition: all 0.15s ease; }
    .stButton > button:hover { background-color: #000000; color: #FFCC00; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; border-bottom: 2px solid #E0E0E0; }
    .stTabs [data-baseweb="tab"] { font-weight: 700; color: #666666; padding: 0.8rem 0; font-size: 1rem; }
    .stTabs [aria-selected="true"] { color: #000000; border-bottom: 3px solid #FFCC00; }
    .stTextArea textarea { border-radius: 12px; border: 1px solid #CCCCCC; }
    .stTextArea textarea:focus { border-color: #FFCC00; box-shadow: 0 0 0 2px rgba(255, 204, 0, 0.3); }
    .streamlit-expanderHeader { font-weight: 700; background-color: #FFF9E0; border-radius: 8px; padding: 0.6rem 1rem; }
    details[open] summary { border-left: 5px solid #FFCC00; }
    .stAlert { border-radius: 12px; }
    .stCodeBlock pre { background-color: #1A1A1A !important; color: #FFCC00 !important; border-radius: 12px; }
    .cl-tag { display: inline-block; background: #FFCC00; color: #000000; font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.7rem; border-radius: 20px; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

DOMAINS = {
    "General": "You are optimizing prompts for general-purpose professional work.",
    "Software Engineering": "You are optimizing prompts for software engineering tasks: code, architecture, debugging, technical documentation. Emphasize correctness, edge cases, and runnable output.",
    "Business and Strategy": "You are optimizing prompts for business strategy, planning, and operations. Emphasize measurable objectives, stakeholders, and actionable deliverables.",
    "Education": "You are optimizing prompts for teaching and learning. Emphasize clarity, scaffolding, learning outcomes, and assessment.",
    "Health": "You are optimizing prompts for health communication and clinical documentation. Emphasize accuracy, safety, and referral to qualified professionals.",
    "Agriculture": "You are optimizing prompts for agricultural extension and agribusiness. Emphasize practical, field-ready guidance and local context.",
    "Government and Public Service": "You are optimizing prompts for public service delivery and policy communication. Emphasize clarity, inclusivity, and accountability.",
    "Creative and Media": "You are optimizing prompts for creative writing, media production, and content strategy. Emphasize audience, tone, and format.",
    "Research and Academia": "You are optimizing prompts for research design, literature, and academic writing. Emphasize rigor, citation practice, and methodology.",
}

META_SYSTEM = """You are a senior prompt engineer. Your job is to convert a user's rough request into a single, production-ready prompt that any capable AI model can follow to deliver high-quality, professional output.

Strict rules:
- Output ONLY the optimized prompt. No preamble, no commentary, no explanation of what you did.
- The prompt you output must be self-contained and directly usable.
- Structure the output prompt with these clearly labeled sections in this order:
  1. ROLE
  2. OBJECTIVE
  3. CONTEXT AND CONSTRAINTS
  4. INPUTS
  5. PROCESS
  6. OUTPUT FORMAT
  7. QUALITY BAR
- In QUALITY BAR, state concrete, checkable criteria the output must satisfy.
- In OUTPUT FORMAT, be explicit about structure so the result is consistent and review-ready.
- Do NOT answer the user's underlying request. Do NOT produce the deliverable. Only produce the prompt.
- If the user's request is ambiguous, resolve it with reasonable defaults and state those defaults inside CONTEXT AND CONSTRAINTS. Do not ask clarifying questions."""

def optimize_prompt(user_input: str, domain: str, tone: str, depth: str) -> str:
    system = META_SYSTEM + "\n\nDomain guidance: " + DOMAINS.get(domain, DOMAINS["General"])
    user_msg = (
        "Domain: " + domain + "\n"
        "Preferred tone: " + tone + "\n"
        "Preferred depth: " + depth + "\n\n"
        "Rough request from the user:\n" + user_input
    )
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.4,
        max_tokens=1500,
    )
    return resp.choices[0].message.content

def transcribe(audio_bytes, filename):
    transcription = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-large-v3-turbo",
        response_format="text",
    )
    return transcription

st.markdown('<span class="cl-tag">CRAFTLINE</span>', unsafe_allow_html=True)
st.title("PROMPT ENGINEER")
st.caption("From rough idea to professional prompt. Clear instructions that produce quality output on any AI model.")

left, right = st.columns([3, 1])

with right:
    domain = st.selectbox("Domain", list(DOMAINS.keys()), index=0)
    tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional", "Conversational"], index=0)
    depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)

with left:
    st.subheader("Describe what you want the AI to produce")
    user_input = st.text_area(
        "Your rough request",
        placeholder="Example: write a proposal for a school computer lab in a rural district, budget-friendly, with a timeline and equipment list",
        height=180,
    )

    st.markdown("**Or speak your request**")
    audio_value = st.audio_input("Record your request")
    if audio_value is not None:
        with st.spinner("Transcribing..."):
            try:
                text = transcribe(audio_value.getvalue(), "request.wav")
                st.session_state["voice_text"] = text
                st.success("Transcribed. Review below and edit if needed.")
                st.text_area("Transcription", value=text, height=120, key="voice_review")
            except Exception as e:
                st.error("Transcription failed: " + str(e))

    if st.button("GENERATE PROMPT", key="gen"):
        final_input = st.session_state.get("voice_text", "").strip() or user_input.strip()
        if not final_input:
            st.warning("Please type or record a request first.")
        else:
            with st.spinner("Building your prompt..."):
                try:
                    result = optimize_prompt(final_input, domain, tone, depth)
                    st.markdown("### Your optimized prompt")
                    st.code(result, language="markdown")
                    st.caption("Copy this prompt into any AI model. It is self-contained and ready to use.")
                except Exception as e:
                    st.error("Generation failed: " + str(e))
