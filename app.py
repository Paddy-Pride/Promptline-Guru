import os
import streamlit as st
from groq import Groq

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Promptline Guru", page_icon=None, layout="wide")

st.markdown("""
<style>
    /* Global Theme */
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }
    
    /* Background: Energetic runner image with a vibrant gradient overlay */
    .stApp { 
        background-image: 
            linear-gradient(135deg, rgba(255, 213, 0, 0.4), rgba(255, 153, 0, 0.3)),
            url('https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Container */
    .block-container { 
        padding: 3rem 2.5rem; 
        max-width: 850px; 
        background: rgba(255, 255, 255, 0.65); /* Frosted glass */
        backdrop-filter: blur(16px); /* The glass blur effect */
        -webkit-backdrop-filter: blur(16px);
        border-radius: 28px; 
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        margin-top: 3rem;
        margin-bottom: 3rem;
    }

    /* App Name Tag */
    .plg-tag { 
        display: inline-block; 
        background: #FFD500; 
        color: #000000; 
        font-weight: 900; 
        font-size: 0.8rem; 
        padding: 0.3rem 1rem; 
        border-radius: 20px; 
        letter-spacing: 0.1em; 
        margin-bottom: 1rem; 
        border: 2px solid #000000;
        text-transform: uppercase;
    }

    /* Typography */
    h1 { 
        font-size: 2.8rem; 
        font-weight: 900; 
        color: #111111; 
        letter-spacing: -0.03em; 
        line-height: 1.1;
        margin-bottom: 0;
        text-transform: uppercase;
    }
    h1 .highlight { color: #FF9900; }
    .subtitle { color: #333333; font-size: 1.05rem; margin-top: 0.5rem; margin-bottom: 2rem; font-weight: 700; }
    
    /* Card Titles */
    .card-title { 
        color: #000000; 
        font-weight: 900; 
        font-size: 1rem; 
        margin-bottom: 0.5rem; 
        text-transform: uppercase; 
        border-left: 4px solid #FF9900; 
        padding-left: 10px;
    }

    /* Input Fields (Also slightly glassy) */
    .stTextArea textarea { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 16px; 
        border: 1px solid rgba(200, 200, 200, 0.5); 
        color: #000000 !important;
        font-size: 1.05rem; 
        backdrop-filter: blur(4px);
    }
    .stTextArea textarea:focus { border-color: #FF9900; box-shadow: 0 0 0 3px rgba(255,153,0,0.2); }
    
    /* Dropdowns */
    .stSelectbox > div > div { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border: 1px solid rgba(200, 200, 200, 0.5); 
        border-radius: 12px; 
        color: #000000 !important;
        font-weight: 700;
    }
    
    /* Action Button */
    .stButton > button { 
        background-color: #FFD500; 
        color: #000000; 
        border: 2px solid #000000; 
        border-radius: 40px; 
        font-weight: 900; 
        text-transform: uppercase;
        padding: 0.8rem 2rem; 
        font-size: 1.1rem; 
        width: 100%; 
        transition: all 0.2s ease;
        margin-top: 1rem;
    }
    .stButton > button:hover { 
        background-color: #FF9900; 
        color: #FFFFFF; 
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,153,0,0.4);
    }
    
    /* AI Tool Buttons */
    .stLinkButton > a { 
        background-color: rgba(255, 255, 255, 0.7); 
        color: #000000; 
        border: 1px solid rgba(200, 200, 200, 0.8); 
        border-radius: 30px; 
        padding: 0.5rem 0.8rem; 
        font-weight: 800; 
        font-size: 0.8rem; 
        text-decoration: none; 
        width: 100%; 
        text-align: center; 
        transition: all 0.15s;
        backdrop-filter: blur(4px);
    }
    .stLinkButton > a:hover { 
        background-color: #FFD500; 
        border-color: #000000; 
        color: #000000;
    }

    /* Output Code Block (Darker glass to stand out) */
    .stCodeBlock pre { 
        background: rgba(20, 20, 20, 0.95) !important; 
        color: #FFD500 !important; 
        border-radius: 16px; 
        border: 2px solid rgba(255, 213, 0, 0.5);
        font-size: 0.95rem;
    }
    
    hr { border-color: rgba(0,0,0,0.1); margin: 2rem 0; }
    .stCaption { color: #444444 !important; font-weight: 600; }
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
# Name brought back to the top
st.markdown('<div class="plg-tag">PROMPTLINE GURU</div>', unsafe_allow_html=True)
st.markdown('<h1>Prompt Better.<br>Build <span class="highlight">Faster.</span></h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)

st.markdown('<div class="card-title">1. Describe Your Goal</div>', unsafe_allow_html=True)
user_text = st.text_area(
    "Type your request",
    placeholder="e.g., Write a grant proposal for a rural health clinic, including a budget breakdown...",
    height=120,
    label_visibility="collapsed",
)

col_up, col_au = st.columns(2)

with col_up:
    st.markdown('<div class="card-title">Or Upload File</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("PDF or TXT", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
    uploaded_text = ""
    if uploaded:
        uploaded_text = extract_file_text(uploaded)
        st.caption("✅ Loaded: " + uploaded.name)

with col_au:
    st.markdown('<div class="card-title">Or Speak</div>', unsafe_allow_html=True)
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

st.markdown('<div class="card-title">2. Set Parameters</div>', unsafe_allow_html=True)
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

    st.markdown('<div class="card-title" style="margin-top: 2rem;">3. Your Professional Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Copy the prompt above using the icon at the top right of the black box.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">4. Open & Paste</div>', unsafe_allow_html=True)
    st.caption("Click a tool below to open it in a new tab. Paste the prompt to generate your result.")

    for row_start in range(0, len(AI_TOOLS), 4):
        row_tools = AI_TOOLS[row_start:row_start + 4]
        cols = st.columns(len(row_tools))
        for i, tool in enumerate(row_tools):
            with cols[i]:
                st.image(tool["icon"], width=36)
                st.link_button(tool["name"], tool["url"], use_container_width=True)
