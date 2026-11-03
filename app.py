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
    {"name": "ChatGPT", "url": "https://chat.openai.com", "icon": "https://chat.openai.com/favicon.ico"},
    {"name": "Claude", "url": "https://claude.ai", "icon": "https://claude.ai/favicon.ico"},
    {"name": "Gemini", "url": "https://gemini.google.com", "icon": "https://www.gstatic.com/devrel-devsite/prod/v5e941f15ff6710591bee254538202655020220785b40a3f4d932e94adb9f6037/googledevai/images/favicon-new.png"},
    {"name": "Grok", "url": "https://grok.com", "icon": "https://grok.com/images/favicon.svg"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "icon": "https://www.deepseek.com/favicon.ico"},
    {"name": "Copilot", "url": "https://copilot.microsoft.com", "icon": "https://copilot.microsoft.com/favicon.ico"},
    {"name": "Perplexity", "url": "https://www.perplexity.ai", "icon": "https://www.perplexity.ai/favicon.ico"},
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
st.caption("Write, upload, or speak. Get a professional prompt. Pick a tool to open and paste.")

c1, c2, c3 = st.columns(3)
with c1: domain = st.selectbox("Domain", list(DOMAINS.keys()))
with c2: tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"])
with c3: depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)

st.markdown("**Your request**")
user_text = st.text_area("", placeholder="Describe what you want the AI to produce...", height=140, label_visibility="collapsed")

btn_col1, btn_col2, _ = st.columns([1, 1, 3])
with btn_col1:
    if st.button("Upload file"):
        st.session_state["show_upload"] = True
with btn_col2:
    if st.button("Speak"):
        st.session_state["show_speak"] = True

if st.session_state.get("show_upload"):
    f = st.file_uploader("Upload txt, md, csv, or pdf", type=["txt", "md", "csv", "pdf"])
    if f:
        st.session_state["file_text"] = extract_file_text(f)
        st.text_area("Extracted (editable)", value=st.session_state["file_text"][:3000], height=120)

if st.session_state.get("show_speak"):
    audio = st.audio_input("Record in English, Luganda, Swahili, or other")
    if audio:
        with st.spinner("Transcribing..."):
            result = client.audio.transcriptions.create(
                file=("req.wav", audio.getvalue()), model="whisper-large-v3", response_format="text"
            )
            st.session_state["voice_text"] = result
            st.text_area("Transcribed (editable)", value=result, height=80)

if st.button("GENERATE PROMPT", key="gen"):
    final = user_text.strip() or st.session_state.get("file_text", "").strip()
    if not final and st.session_state.get("voice_text"):
        with st.spinner("Translating..."):
            final = translate_to_english(st.session_state["voice_text"])
    if not final:
        st.warning("Provide a request first.")
        st.stop()

    with st.spinner("Building prompt..."):
        prompt = optimize_prompt(final, domain, tone, depth)

    st.markdown("### Your prompt")
    st.code(prompt, language="markdown")
    st.caption("Click the copy icon at the top right of the code block to copy the prompt.")

    st.markdown("### Open in your AI tool")
    st.caption("Copy the prompt above, then click any tool below to open it and paste with Ctrl+V.")

    # Render icons and link buttons natively, no iframe.
    for row_start in range(0, len(AI_TOOLS), 4):
        row_tools = AI_TOOLS[row_start:row_start + 4]
        cols = st.columns(len(row_tools))
        for i, tool in enumerate(row_tools):
            with cols[i]:
                try:
                    st.image(tool["icon"], width=40)
                except Exception:
                    st.markdown("**" + tool["name"][0] + "**")
                st.link_button(tool["name"], tool["url"], use_container_width=True)
