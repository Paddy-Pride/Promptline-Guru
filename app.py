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
    h1 { font-size: 2.2rem; border-bottom: 4px solid #FFCC00; padding-bottom: 0.4rem; display: inline-block; color: #000; font-weight: 700; }
    .stButton > button { background-color: #FFCC00; color: #000; border: 2px solid #000; border-radius: 30px; font-weight: 700; padding: 0.6rem 1.8rem; }
    .stButton > button:hover { background-color: #000; color: #FFCC00; }
    .stLinkButton > a { background-color: #FFF9E0; color: #000; border: 1px solid #E0E0E0; border-radius: 12px; padding: 0.5rem 1rem; font-weight: 700; font-size: 0.85rem; text-decoration: none; width: 100%; text-align: center; }
    .stLinkButton > a:hover { background-color: #FFCC00; border-color: #FFCC00; }
    .stTextArea textarea { border-radius: 12px; border: 1px solid #CCC; }
    .stTextArea textarea:focus { border-color: #FFCC00; box-shadow: 0 0 0 2px rgba(255,204,0,0.3); }
    .stCodeBlock pre { background: #1A1A1A !important; color: #FFCC00 !important; border-radius: 12px; }
    .plg-tag { display: inline-block; background: #FFCC00; color: #000; font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.7rem; border-radius: 20px; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
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

st.markdown('<span class="plg-tag">PROMPTLINE GURU</span>', unsafe_allow_html=True)
st.title("PROMPT ENGINEER")
st.caption("Type, upload, or speak. Get a professional prompt. Pick a tool to open and paste.")

c1, c2, c3 = st.columns(3)
with c1: domain = st.selectbox("Domain", list(DOMAINS.keys()))
with c2: tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"])
with c3: depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)

st.markdown("### Your request")
user_text = st.text_area(
    "Type your request here",
    placeholder="Example: write a proposal for a school computer lab in a rural district, budget-friendly, with a timeline and equipment list",
    height=160,
    label_visibility="collapsed",
)

# Three input columns beneath the textarea: upload, audio, and a spacer
col_up, col_au = st.columns(2)

with col_up:
    st.markdown("**Upload a file**")
    uploaded = st.file_uploader(
        "Choose txt, md, csv, or pdf",
        type=["txt", "md", "csv", "pdf"],
        label_visibility="collapsed",
    )
    uploaded_text = ""
    if uploaded:
        uploaded_text = extract_file_text(uploaded)
        st.caption("Loaded: " + uploaded.name + " (" + str(len(uploaded_text)) + " characters)")

with col_au:
    st.markdown("**Record your request**")
    audio_value = st.audio_input("Record", label_visibility="collapsed")
    voice_text = ""
    if audio_value is not None:
        with st.spinner("Transcribing..."):
            try:
                voice_text = client.audio.transcriptions.create(
                    file=("req.wav", audio_value.getvalue()),
                    model="whisper-large-v3",
                    response_format="text",
                )
                st.caption("Transcribed: " + voice_text[:120])
            except Exception as e:
                st.error("Transcription failed: " + str(e))

if st.button("GENERATE PROMPT", key="gen"):
    final = user_text.strip()
    if not final and uploaded_text.strip():
        final = uploaded_text.strip()
    if not final and voice_text:
        with st.spinner("Translating..."):
            final = translate_to_english(voice_text)
    if not final:
        st.warning("Type a request, upload a file, or record audio first.")
        st.stop()

    with st.spinner("Building prompt..."):
        prompt = optimize_prompt(final, domain, tone, depth)

    st.markdown("### Your prompt")
    st.code(prompt, language="markdown")
    st.caption("Use the copy icon at the top right of the code block to copy.")

    st.markdown("### Open in your AI tool")
    st.caption("Copy the prompt above, then click a tool below to open it. Paste with Ctrl+V.")

    for row_start in range(0, len(AI_TOOLS), 4):
        row_tools = AI_TOOLS[row_start:row_start + 4]
        cols = st.columns(len(row_tools))
        for i, tool in enumerate(row_tools):
            with cols[i]:
                st.image(tool["icon"], width=40)
                st.link_button(tool["name"], tool["url"], use_container_width=True)
