import os
import streamlit as st
from groq import Groq

# ============================================================
# Promptline Guru
# Plain language in, professional AI instructions out.
# Upload, Ugandan voice, multi-AI routing.
# Groq API only. No emojis. MTN Pulse styling.
# ============================================================

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="Promptline Guru",
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
    .plg-tag { display: inline-block; background: #FFCC00; color: #000000; font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.7rem; border-radius: 20px; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .ai-btn { display: inline-block; background: #F5F5F5; color: #000000; font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem 0.4rem 0.25rem 0; border: 1px solid #DDDDDD; text-decoration: none; }
    .ai-btn:hover { background: #FFCC00; border-color: #FFCC00; color: #000000; }
</style>
""", unsafe_allow_html=True)

DOMAINS = {
    "General": "You are optimizing prompts for general-purpose professional work.",
    "Software Engineering": "You are optimizing prompts for software engineering tasks. Emphasize correctness, edge cases, and runnable output.",
    "Business and Strategy": "You are optimizing prompts for business strategy and operations. Emphasize measurable objectives and actionable deliverables.",
    "Education": "You are optimizing prompts for teaching and learning. Emphasize clarity, scaffolding, and assessment.",
    "Health": "You are optimizing prompts for health communication. Emphasize accuracy, safety, and referral to professionals.",
    "Agriculture": "You are optimizing prompts for agricultural extension. Emphasize practical, field-ready guidance.",
    "Government and Public Service": "You are optimizing prompts for public service delivery. Emphasize clarity, inclusivity, and accountability.",
    "Creative and Media": "You are optimizing prompts for creative work. Emphasize audience, tone, and format.",
    "Research and Academia": "You are optimizing prompts for research. Emphasize rigor and methodology.",
}

AI_TOOLS = [
    {"name": "ChatGPT", "url": "https://chat.openai.com", "color": "#10A37F"},
    {"name": "Claude", "url": "https://claude.ai", "color": "#D97757"},
    {"name": "Gemini", "url": "https://gemini.google.com", "color": "#4285F4"},
    {"name": "Grok", "url": "https://grok.com", "color": "#000000"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "color": "#4D6BFE"},
    {"name": "Copilot", "url": "https://copilot.microsoft.com", "color": "#0078D4"},
    {"name": "Perplexity", "url": "https://perplexity.ai", "color": "#20808D"},
]

META_SYSTEM = """You are a senior prompt engineer. Convert a user's rough request into a single, production-ready prompt.

Strict rules:
- Output ONLY the optimized prompt. No preamble.
- Structure: ROLE, OBJECTIVE, CONTEXT AND CONSTRAINTS, INPUTS, PROCESS, OUTPUT FORMAT, QUALITY BAR.
- QUALITY BAR must state concrete, checkable criteria.
- Do NOT answer the user's request. Only produce the prompt.
- Resolve ambiguity with stated defaults. Do not ask questions."""

def optimize_prompt(user_input: str, domain: str, tone: str, depth: str) -> str:
    system = META_SYSTEM + "\n\nDomain: " + DOMAINS.get(domain, DOMAINS["General"])
    user_msg = (
        "Domain: " + domain + "\nTone: " + tone + "\nDepth: " + depth + "\n\n"
        "Rough request:\n" + user_input
    )
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user_msg}],
        temperature=0.4,
        max_tokens=1500,
    )
    return resp.choices[0].message.content

def transcribe_audio(audio_bytes, filename):
    """Transcribe in original language. Auto-detect for unsupported Ugandan languages."""
    result = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-large-v3",
        response_format="text",
    )
    return result

def translate_to_english(text: str) -> str:
    """Groq LLM translates any text to English. Used for Ugandan languages not directly supported."""
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Translate the following text to English. Output only the translation, no explanation. If already English, output unchanged."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
        max_tokens=800,
    )
    return resp.choices[0].message.content.strip()

def extract_file_text(uploaded_file) -> str:
    """Extract text from uploaded txt, md, csv, or pdf."""
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()
    if name.endswith(".pdf"):
        try:
            import fitz
            doc = fitz.open(stream=data, filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except ImportError:
            return "[PDF support requires PyMuPDF. Install with: pip install PyMuPDF]"
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return "[Could not decode file as text]"

st.markdown('<span class="plg-tag">PROMPTLINE GURU</span>', unsafe_allow_html=True)
st.title("PROMPT ENGINEER")
st.caption("Plain language in, professional AI instructions out. Text, voice, or file upload. Any domain.")

# ---------- AI Tool Selector (visual, no trademarked icons) ----------
st.markdown("**Where will you paste this prompt?**")
cols = st.columns(len(AI_TOOLS))
for i, tool in enumerate(AI_TOOLS):
    with cols[i]:
        st.markdown(
            '<a href="' + tool["url"] + '" target="_blank" class="ai-btn" style="border-left: 4px solid ' + tool["color"] + ';">' + tool["name"] + '</a>',
            unsafe_allow_html=True,
        )
st.caption("Click a tool to open it. Generate your prompt below, then paste it into any tool.")

# ---------- Controls ----------
right = st.container()
with right:
    c1, c2, c3 = st.columns(3)
    with c1:
        domain = st.selectbox("Domain", list(DOMAINS.keys()), index=0)
    with c2:
        tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional", "Conversational"], index=0)
    with c3:
        depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)

# ---------- Input Tabs ----------
input_tab1, input_tab2, input_tab3 = st.tabs(["TYPE", "UPLOAD FILE", "SPEAK"])

with input_tab1:
    user_input = st.text_area(
        "Describe what you want the AI to produce",
        placeholder="Example: write a proposal for a school computer lab in a rural district, budget-friendly, with a timeline and equipment list",
        height=160,
    )

with input_tab2:
    uploaded = st.file_uploader("Upload a text, markdown, CSV, or PDF file", type=["txt", "md", "csv", "pdf"])
    if uploaded is not None:
        with st.spinner("Extracting text..."):
            file_text = extract_file_text(uploaded)
        st.session_state["file_text"] = file_text
        st.text_area("Extracted content (edit if needed)", value=file_text[:4000], height=200)
        st.caption("The full extracted text will be used if you generate from this tab.")

with input_tab3:
    st.markdown("**Speak in English, Luganda, Swahili, or any supported language.**")
    st.caption("Groq Whisper supports 99+ languages. For smaller Ugandan languages not on the supported list, auto-detection may produce lower accuracy. Text will be translated to English before optimization.")
    audio_value = st.audio_input("Record your request")
    if audio_value is not None:
        with st.spinner("Transcribing..."):
            try:
                transcribed = transcribe_audio(audio_value.getvalue(), "request.wav")
                st.session_state["voice_raw"] = transcribed
                st.success("Transcribed. Review and edit below.")
                edited = st.text_area("Original transcription (edit if needed)", value=transcribed, height=100, key="voice_edit")
                st.session_state["voice_text"] = edited
            except Exception as e:
                st.error("Transcription failed: " + str(e))

# ---------- Generate ----------
if st.button("GENERATE PROMPT", key="gen"):
    final_input = ""
    source = ""

    typed = user_input.strip() if user_input else ""
    file_ready = st.session_state.get("file_text", "").strip()
    voice_ready = st.session_state.get("voice_text", "").strip()

    if typed:
        final_input = typed
        source = "typed"
    elif file_ready:
        final_input = file_ready
        source = "file"
    elif voice_ready:
        source = "voice"
        with st.spinner("Translating to English..."):
            try:
                final_input = translate_to_english(voice_ready)
                st.caption("Translated input: " + final_input[:300])
            except Exception:
                final_input = voice_ready
    else:
        st.warning("Please type, upload, or speak a request first.")
        st.stop()

    with st.spinner("Building your prompt..."):
        try:
            result = optimize_prompt(final_input, domain, tone, depth)
            st.markdown("### Your optimized prompt")
            st.code(result, language="markdown")
            st.caption("Copy this prompt into ChatGPT, Claude, Gemini, Grok, DeepSeek, Copilot, or any AI tool. It is self-contained.")
        except Exception as e:
            st.error("Generation failed: " + str(e))

# ---------- Footer ----------
st.markdown("---")
st.caption("Promptline Guru. Built on Groq. Voice via Whisper. No data stored.")
