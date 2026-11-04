import os
import streamlit as st
from groq import Groq

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Promptline Guru", page_icon=None, layout="wide")

st.markdown("""
<style>
    /* Global Theme: Deep Teal / Dark Mode */
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }
    .stApp { background-color: #1E2F30; /* MTN Pulse Dark Teal */ }
    
    /* Main Layout Container */
    .block-container { 
        padding-top: 2rem; 
        max-width: 900px; 
        background-color: #111B1C; 
        border-radius: 24px; 
        padding-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid #2A3E40;
        margin-top: 2rem;
    }

    /* Typography: Heavy, Italicized, Punchy */
    h1 { 
        font-size: 3rem; 
        font-weight: 900; 
        font-style: italic;
        color: #FFFFFF; 
        letter-spacing: -0.04em; 
        line-height: 1.05;
        margin-bottom: 0;
        text-transform: uppercase;
    }
    h1 .highlight { color: #FFD500; /* Electric Yellow */ }
    .subtitle { color: #A0B0B0; font-size: 1rem; margin-top: 0.5rem; margin-bottom: 2rem; font-weight: 600; }
    
    /* Text Elements */
    p, label, .stMarkdown { color: #E0E0E0 !important; }
    .card-title { color: #FFD500; font-weight: 900; font-style: italic; font-size: 1.2rem; margin-bottom: 0.5rem; text-transform: uppercase;}

    /* Input Fields */
    .stTextArea textarea { 
        background-color: #1A282A !important; 
        border-radius: 16px; 
        border: 2px solid #3A5052; 
        color: #FFFFFF !important;
        font-size: 1rem; 
    }
    .stTextArea textarea:focus { border-color: #FF9900; box-shadow: 0 0 0 3px rgba(255,153,0,0.2); }
    
    /* Dropdowns */
    .stSelectbox > div > div { 
        background-color: #1A282A !important; 
        border: 2px solid #3A5052; 
        border-radius: 12px; 
        color: #FFFFFF !important;
    }
    
    /* The Main Action Button */
    .stButton > button { 
        background-color: #FF9900; /* Vibrant Orange */
        color: #FFFFFF; 
        border: none; 
        border-radius: 40px; 
        font-weight: 900; 
        font-style: italic;
        text-transform: uppercase;
        padding: 0.8rem 2rem; 
        font-size: 1.2rem; 
        width: 100%; 
        transition: all 0.15s ease;
        margin-top: 1rem;
    }
    .stButton > button:hover { 
        background-color: #FFD500; /* Yellow on hover */
        color: #111B1C; 
        transform: scale(1.02);
    }
    
    /* AI Tool Link Buttons */
    .stLinkButton > a { 
        background-color: #1A282A; 
        color: #FFFFFF; 
        border: 2px solid #3A5052; 
        border-radius: 30px; 
        padding: 0.5rem 0.8rem; 
        font-weight: 700; 
        font-size: 0.8rem; 
        text-decoration: none; 
        width: 100%; 
        text-align: center; 
        transition: all 0.15s;
    }
    .stLinkButton > a:hover { 
        background-color: #FF9900; 
        border-color: #FF9900; 
        color: #FFFFFF;
    }

    /* Output Code Block */
    .stCodeBlock pre { 
        background: #000000 !important; 
        color: #FFD500 !important; 
        border-radius: 16px; 
        border: 2px solid #FFD500;
        font-size: 0.95rem;
    }

    /* Expandable Note (Audio / Upload) */
    .stAlert { 
        background-color: #1A282A; 
        border-radius: 16px; 
        border-left: 6px solid #FFD500; 
        color: #FFFFFF;
    }
    
    /* Subtle Dividers */
    hr { border-color: #2A3E40; }
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

GROQ_LANGS = {"English": "en", "Swahili": "sw", "French": "fr", "Arabic": "ar", "Portuguese": "pt", "Spanish": "es"}

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
st.markdown('<h1>Unleash the power of<br><span class="highlight">professional prompts</span></h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type, upload, or speak. Let AI do the heavy lifting.</div>', unsafe_allow_html=True)

st.markdown('<div class="card-title">What do you want to create?</div>', unsafe_allow_html=True)
user_text = st.text_area(
    "Type your request",
    placeholder="e.g., write a proposal for a school computer lab...",
    height=120,
    label_visibility="collapsed",
)

# Upload & Audio Grid
col_up, col_au = st.columns(2)

with col_up:
    st.markdown('<div class="card-title">Upload Context</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("PDF or TXT", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
    uploaded_text = ""
    if uploaded:
        uploaded_text = extract_file_text(uploaded)
        st.caption("✅ Loaded: " + uploaded.name)

with col_au:
    st.markdown('<div class="card-title">Speak</div>', unsafe_allow_html=True)
    lang_name = st.selectbox("Audio language", list(GROQ_LANGS.keys()), index=0, label_visibility="collapsed")
    audio_value = st.audio_input("Record", label_visibility="collapsed")
    voice_text = ""
    if audio_value is not None:
        with st.spinner("Transcribing..."):
            try:
                voice_text = client.audio.transcriptions.create(
                    file=("req.wav", audio_value.getvalue()),
                    model="whisper-large-v3",
                    language=GROQ_LANGS[lang_name],
                    response_format="text",
                )
                st.caption("✅ Transcribed: " + voice_text[:30] + "...")
            except Exception as e:
                st.error("Transcription failed: " + str(e))
    st.caption("Note: For Leb Lango, please type instead. Whisper does not support it directly.")

st.markdown("<hr>", unsafe_allow_html=True)

# Controls
c1, c2, c3 = st.columns(3)
with c1: domain = st.selectbox("Domain", list(DOMAINS.keys()))
with c2: tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"])
with c3: depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)

# Generate Button
if st.button("GENERATE PROMPT", key="gen"):
    final = user_text.strip() or uploaded_text.strip()
    if not final and voice_text:
        with st.spinner("Translating..."):
            final = translate_to_english(voice_text)
    if not final:
        st.warning("Please provide a request first.")
        st.stop()

    with st.spinner("Forging..."):
        prompt = optimize_prompt(final, domain, tone, depth)

    st.markdown('<div class="card-title" style="margin-top: 2rem;">Your Custom Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Copy the prompt above using the icon at the top right.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Open & Paste</div>', unsafe_allow_html=True)
    st.caption("Click a tool below to open it in a new tab. Paste the prompt to generate your result.")

    # Render AI Tools in a single neat row
    for row_start in range(0, len(AI_TOOLS), 4):
        row_tools = AI_TOOLS[row_start:row_start + 4]
        cols = st.columns(len(row_tools))
        for i, tool in enumerate(row_tools):
            with cols[i]:
                st.image(tool["icon"], width=36)
                st.link_button(tool["name"], tool["url"], use_container_width=True)
