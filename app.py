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
    
    /* Background: Energetic runner image with vibrant MTN overlay */
    .stApp { 
        background-image: 
            linear-gradient(135deg, rgba(255, 213, 0, 0.45), rgba(255, 153, 0, 0.35)),
            url('https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Main Container */
    .block-container { 
        padding: 3rem 2.5rem; 
        max-width: 900px; 
        background: rgba(255, 255, 255, 0.70);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 28px; 
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        margin-top: 3rem;
        margin-bottom: 3rem;
    }

    /* Glassmorphism Sidebar (Left Margin) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.6);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #000000;
        font-weight: 900;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #111111 !important;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 0.85rem;
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
    
    /* Chat Input Customization */
    [data-testid="stChatInput"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD500 !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #FF9900 !important;
        box-shadow: 0 0 0 3px rgba(255,153,0,0.2) !important;
    }

    /* Audio Input Customization */
    [data-testid="stAudioInput"] {
        background-color: transparent !important;
        padding: 0;
    }
    [data-testid="stAudioInput"] button {
        border-radius: 50% !important;
        background-color: #FFD500 !important;
        color: #000 !important;
        border: 2px solid #000 !important;
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
        background-color: rgba(255, 255, 255, 0.8); 
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

    /* Output Code Block */
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

# ========== Sidebar (Left Margin) Parameters ==========
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Settings</h2>", unsafe_allow_html=True)
    st.markdown("---")
    domain = st.selectbox("Domain", list(DOMAINS.keys()))
    tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"])
    depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)
    st.markdown("---")
    
    lang_name = st.selectbox("Audio Language", list(GROQ_LANGS.keys()), index=0)
    st.caption("Note: For Leb Lango, please type instead. Whisper does not support it directly.")

# ========== UI Main ==========
st.markdown('<div class="plg-tag">PROMPTLINE GURU</div>', unsafe_allow_html=True)
st.markdown('<h1>Prompt Better.<br>Build <span class="highlight">Faster.</span></h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)

# Integrated Chat Box + Audio Recorder
st.markdown("**Your Request**")
st.caption("Use the paperclip to upload a document, or the microphone to speak.")

col_chat, col_audio = st.columns([4, 1])

with col_chat:
    # Accept file=True adds the upload icon directly inside the chat box
    chat_val = st.chat_input("Type your request here...", accept_file=True, file_type=["txt", "md", "csv", "pdf"])

with col_audio:
    # Small audio recorder acting as the mic icon
    audio_value = st.audio_input("Speak", label_visibility="collapsed")

# Process Inputs
final_text = ""
uploaded_text = ""
voice_text = ""

if chat_val:
    if chat_val.text:
        final_text = chat_val.text
    if chat_val.files:
        for f in chat_val.files:
            uploaded_text += extract_file_text(f)

if audio_value is not None:
    with st.spinner("Transcribing audio..."):
        try:
            voice_text = client.audio.transcriptions.create(
                file=("req.wav", audio_value.getvalue()),
                model="whisper-large-v3",
                language=GROQ_LANGS[lang_name],
                response_format="text",
            )
            st.caption("✅ Transcribed: " + voice_text[:50] + "...")
        except Exception as e:
            st.error("Transcription failed: " + str(e))

st.markdown("<br>", unsafe_allow_html=True)

if st.button("GENERATE PROMPT", key="gen"):
    # Determine which input to use
    final_input = final_text.strip() or uploaded_text.strip()
    
    if not final_input and voice_text:
        with st.spinner("Translating..."):
            final_input = translate_to_english(voice_text)
            
    if not final_input:
        st.warning("Please type a request, upload a file, or record audio first.")
        st.stop()

    with st.spinner("Forging your prompt..."):
        prompt = optimize_prompt(final_input, domain, tone, depth)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Professional Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Copy the prompt above using the icon at the top right of the black box.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Open & Paste</div>', unsafe_allow_html=True)
    st.caption("Click a tool below to open it in a new tab. Paste the prompt to generate your result.")

    # Render AI Tools
    for row_start in range(0, len(AI_TOOLS), 4):
        row_tools = AI_TOOLS[row_start:row_start + 4]
        cols = st.columns(len(row_tools))
        for i, tool in enumerate(row_tools):
            with cols[i]:
                st.image(tool["icon"], width=36)
                st.link_button(tool["name"], tool["url"], use_container_width=True)
