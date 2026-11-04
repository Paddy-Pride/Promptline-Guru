import os
import streamlit as st
from groq import Groq

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Promptline Guru", page_icon=None, layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }
    .stApp { background-color: #FFFFFF; }
    .block-container { padding-top: 3rem; max-width: 900px; }
    h1 { font-size: 2.2rem; font-weight: 900; color: #000; letter-spacing: -0.03em; margin-bottom: 0; }
    .subtitle { color: #666; font-size: 1rem; margin-top: 0.2rem; margin-bottom: 1.5rem; }
    .yellow-bar { height: 6px; background: #FFCC00; border-radius: 3px; margin: 0.6rem 0 1.5rem 0; width: 80px; }
    .stButton > button { background: #FFCC00; color: #000; border: 3px solid #000; border-radius: 40px; font-weight: 800; padding: 0.7rem 2rem; font-size: 1rem; width: 100%; }
    .stButton > button:hover { background: #000; color: #FFCC00; }
    .stLinkButton > a { background: #FFF9E0; color: #000; border: 2px solid #E0E0E0; border-radius: 12px; padding: 0.5rem 0.8rem; font-weight: 800; font-size: 0.8rem; text-decoration: none; width: 100%; text-align: center; }
    .stLinkButton > a:hover { background: #FFCC00; border-color: #000; }
    .stTextArea textarea { border-radius: 14px; border: 2px solid #CCC; font-size: 1rem; }
    .stTextArea textarea:focus { border-color: #FFCC00; box-shadow: 0 0 0 3px rgba(255,204,0,0.25); }
    .stCodeBlock pre { background: #1A1A1A !important; color: #FFCC00 !important; border-radius: 14px; border: 2px solid #FFCC00; }
    .plg-tag { display: inline-block; background: #FFCC00; color: #000; font-weight: 900; font-size: 0.7rem; padding: 0.2rem 0.8rem; border-radius: 20px; letter-spacing: 0.08em; margin-bottom: 0.4rem; border: 2px solid #000; }
    .stAlert { border-radius: 12px; }
    .stExpander { border: 1px solid #E0E0E0; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

DOMAINS = {
    "General": "General-purpose professional work.",
    "Software Engineering": "Code, architecture, debugging. Emphasize correctness and runnable output.",
    "Business and Strategy": "Strategy, planning, operations. Emphasize measurable objectives.",
    "Education": "Teaching and learning. Emphasize clarity and assessment.",
    "Health": "Health communication. Emphasize accuracy and safety.",
    "Agriculture": "Agricultural extension. Emphasize field-ready guidance.",
    "Government": "Public service delivery. Emphasize clarity and accountability.",
}

GROQ_LANGS = {"English": "en", "Swahili": "sw", "French": "fr", "Arabic": "ar"}

AI_TOOLS = [
    {"name": "ChatGPT", "url": "https://chat.openai.com", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/openai.webp"},
    {"name": "Claude", "url": "https://claude.ai", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/claude.webp"},
    {"name": "Gemini", "url": "https://gemini.google.com", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/gemini.webp"},
    {"name": "Grok", "url": "https://grok.com", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/grok.webp"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/deepseek.webp"},
    {"name": "Copilot", "url": "https://copilot.microsoft.com", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/copilot.webp"},
    {"name": "Perplexity", "url": "https://www.perplexity.ai", "icon": "https://unpkg.com/@lobehub/icons-static-avatar@latest/avatars/perplexity.webp"},
]

META_SYSTEM = """You are a senior prompt engineer. Convert a rough request into a production-ready prompt.
Output ONLY the prompt. Structure: ROLE, OBJECTIVE, CONTEXT AND CONSTRAINTS, INPUTS, PROCESS, OUTPUT FORMAT, QUALITY BAR.
QUALITY BAR must contain concrete, checkable criteria.
Do NOT answer the user's request. Resolve ambiguity with stated defaults."""

def optimize_prompt(user_input, domain, tone, depth):
    system = META_SYSTEM + "\n\nDomain: " + DOMAINS.get(domain, DOMAINS["General"])
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": "Domain: " + domain + "\nTone: " + tone + "\nDepth: " + depth + "\n\nRequest:\n" + user_input},
        ],
        temperature=0.4, max_tokens=1500,
    )
    return resp.choices[0].message.content

def translate_to_english(text):
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Translate to English. Output only the translation."},
            {"role": "user", "content": text},
        ], temperature=0.1, max_tokens=800,
    )
    return resp.choices[0].message.content.strip()

def extract_file_text(f):
    name = f.name.lower()
    data = f.getvalue()
    if name.endswith(".pdf"):
        import fitz
        doc = fitz.open(stream=data, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    return data.decode("utf-8", errors="replace")

# ========== UI ==========
st.markdown('<span class="plg-tag">PROMPTLINE GURU</span>', unsafe_allow_html=True)
st.markdown('<h1>Professional prompts, in one step.</h1>', unsafe_allow_html=True)
st.markdown('<div class="yellow-bar"></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Describe what you want. We write the prompt. You use it in any AI.</div>', unsafe_allow_html=True)

user_text = st.text_area(
    "What do you want the AI to produce?",
    placeholder="Example: write a proposal for a school computer lab in a rural district, budget-friendly, with a timeline and equipment list",
    height=130,
    label_visibility="collapsed",
)

c1, c2, c3 = st.columns(3)
with c1: domain = st.selectbox("Domain", list(DOMAINS.keys()), label_visibility="collapsed")
with c2: tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"], label_visibility="collapsed")
with c3: depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1, label_visibility="collapsed")

# Collapsed secondary inputs
with st.expander("Add a file or record audio"):
    sub1, sub2 = st.columns(2)
    uploaded_text = ""
    voice_text = ""
    with sub1:
        uploaded = st.file_uploader("Upload txt, md, csv, or pdf", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
        if uploaded:
            uploaded_text = extract_file_text(uploaded)
            st.caption("Loaded: " + uploaded.name)
    with sub2:
        st.caption("Groq Whisper supports English, Swahili, French, Arabic. Other Ugandan languages: type instead.")
        lang_name = st.selectbox("Audio language", list(GROQ_LANGS.keys()), label_visibility="collapsed")
        audio_value = st.audio_input("Record", label_visibility="collapsed")
        if audio_value is not None:
            with st.spinner("Transcribing..."):
                try:
                    voice_text = client.audio.transcriptions.create(
                        file=("req.wav", audio_value.getvalue()),
                        model="whisper-large-v3",
                        language=GROQ_LANGS[lang_name],
                        response_format="text",
                    )
                    st.caption("Transcribed: " + voice_text[:100])
                except Exception as e:
                    st.error("Transcription failed: " + str(e))

if st.button("GENERATE PROMPT", key="gen"):
    final = user_text.strip() or uploaded_text.strip()
    if not final and voice_text:
        with st.spinner("Translating..."):
            final = translate_to_english(voice_text)
    if not final:
        st.warning("Type a request first.")
        st.stop()

    with st.spinner("Building prompt..."):
        prompt = optimize_prompt(final, domain, tone, depth)

    st.markdown("### Your prompt")
    st.code(prompt, language="markdown")
    st.caption("Copy with the icon at the top right of the code block.")

    st.markdown("### Open in your AI tool")
    row = st.columns(len(AI_TOOLS))
    for i, tool in enumerate(AI_TOOLS):
        with row[i]:
            st.image(tool["icon"], width=32)
            st.link_button(tool["name"], tool["url"], use_container_width=True)
