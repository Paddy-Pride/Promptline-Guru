import os
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Promptline Guru", page_icon=None, layout="wide")

st.markdown("""
<style>
    /* Global Theme */
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }
    
    /* Background */
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
        padding: 1.5rem 2.5rem; 
        max-width: 900px; 
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 28px; 
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.6);
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
        font-size: 1rem; 
        padding: 0.4rem 1.2rem; 
        border-radius: 25px; 
        letter-spacing: 0.1em; 
        margin-bottom: 0.8rem; 
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
    .subtitle { color: #333333; font-size: 1.05rem; margin-top: 0.5rem; margin-bottom: 1rem; font-weight: 700; }

    /* Typewriter Message Box */
    .typewriter-container {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #FFD500;
        border-radius: 12px;
        padding: 10px 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        display: inline-block;
        min-width: 300px;
    }
    .typewriter-text {
        color: #000000;
        font-weight: 800;
        font-size: 1rem;
        font-family: monospace;
        text-transform: uppercase;
        margin: 0;
    }

    /* Input Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: rgba(255,255,255,0.6);
        padding: 5px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 800;
        color: #333;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD500 !important;
        color: #000 !important;
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
        margin-top: 0.5rem;
    }
    .stButton > button:hover { 
        background-color: #FF9900; 
        color: #FFFFFF; 
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,153,0,0.4);
    }
    
    /* AI Tool Cards */
    .ai-card { 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background-color: rgba(255, 255, 255, 0.95); 
        border: 2px solid #E0E0E0; 
        border-radius: 16px; 
        padding: 1rem 0.5rem; 
        text-decoration: none; 
        color: #000; 
        transition: all 0.2s;
        height: 100%;
    }
    .ai-card:hover { 
        border-color: #FFD500; 
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .ai-logo { width: 36px; height: 36px; margin-bottom: 8px; object-fit: contain; }
    .ai-name { font-weight: 800; font-size: 0.8rem; text-align: center; margin: 0; }
    .ai-fallback { 
        width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 1.2rem; color: #FFF; margin-bottom: 8px;
    }

    /* Output Code Block */
    .stCodeBlock pre { 
        background: rgba(20, 20, 20, 0.95) !important; 
        color: #FFD500 !important; 
        border-radius: 16px; 
        border: 2px solid rgba(255, 213, 0, 0.5);
        font-size: 0.95rem;
    }
    
    hr { border-color: rgba(0,0,0,0.1); margin: 1.5rem 0; }
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
    {"name": "ChatGPT", "url": "https://chat.openai.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/openai.png", "color": "#10A37F", "initial": "C"},
    {"name": "Claude", "url": "https://claude.ai", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/claude.png", "color": "#D97757", "initial": "C"},
    {"name": "Gemini", "url": "https://gemini.google.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/gemini.png", "color": "#4285F4", "initial": "G"},
    {"name": "Grok", "url": "https://grok.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/grok.png", "color": "#000000", "initial": "G"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/deepseek.png", "color": "#4D6BFE", "initial": "D"},
    {"name": "Copilot", "url": "https://copilot.microsoft.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/copilot.png", "color": "#0078D4", "initial": "C"},
    {"name": "Perplexity", "url": "https://www.perplexity.ai", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/light/perplexity.png", "color": "#20808D", "initial": "P"},
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

# ========== Sidebar Settings ==========
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

# Typewriter Animation Component
typewriter_html = """
<div class="typewriter-container">
    <p class="typewriter-text" id="typewriter"></p>
</div>
<script>
    const texts = [
        "Industry-Grade Production Prompt Engineering",
        "A Better Way to Work with Generative AI",
        "Save Time from Frustrating AI Outputs"
    ];
    let count = 0, index = 0, currentText = "", letter = "", isDeleting = false;
    (function type() {
        if (count === texts.length) count = 0;
        currentText = texts[count];
        if (isDeleting) { letter = currentText.slice(0, --index); } 
        else { letter = currentText.slice(0, ++index); }
        document.getElementById("typewriter").textContent = letter;
        let typeSpeed = isDeleting ? 20 : 60;
        if (!isDeleting && letter.length === currentText.length) { typeSpeed = 2000; isDeleting = true; } 
        else if (isDeleting && letter.length === 0) { isDeleting = false; count++; typeSpeed = 500; }
        setTimeout(type, typeSpeed);
    })();
</script>
"""
components.html(typewriter_html, height=60)

st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)

# Input Tabs for clear state management
tab_type, tab_upload, tab_speak = st.tabs(["Type Request", "Upload File", "Speak Request"])

final_input_text = ""

with tab_type:
    typed_text = st.text_area("What do you want the AI to produce?", height=100, label_visibility="collapsed", placeholder="Type your request here...")
    if typed_text.strip():
        final_input_text = typed_text.strip()
        st.session_state["saved_prompt"] = final_input_text

with tab_upload:
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
    if uploaded_file:
        uploaded_text = extract_file_text(uploaded_file)
        st.caption("✅ Loaded: " + uploaded_file.name)
        final_input_text = uploaded_text.strip()
        st.session_state["saved_prompt"] = final_input_text

with tab_speak:
    st.markdown("Record your voice, then click Process Audio.")
    audio_value = st.audio_input("Record", label_visibility="collapsed")
    if audio_value is not None:
        if st.button("Process Audio"):
            with st.spinner("Transcribing..."):
                try:
                    voice_text = client.audio.transcriptions.create(
                        file=("req.wav", audio_value.getvalue()),
                        model="whisper-large-v3",
                        language=GROQ_LANGS[lang_name],
                        response_format="text",
                    )
                    with st.spinner("Translating..."):
                        translated = translate_to_english(voice_text)
                    st.session_state["saved_prompt"] = translated
                    st.success("✅ Audio Transcribed & Saved!")
                    st.info("**Text:** " + translated)
                except Exception as e:
                    st.error("Transcription failed: " + str(e))

# Show what is currently saved to be generated
if st.session_state.get("saved_prompt"):
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Ready to generate from the text above.")

if st.button("GENERATE PROMPT", key="gen"):
    final_input = st.session_state.get("saved_prompt", "").strip()
    
    if not final_input:
        st.warning("Please type a request, upload a file, or record audio first.")
        st.stop()

    with st.spinner("Forging your prompt..."):
        prompt = optimize_prompt(final_input, domain, tone, depth)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Professional Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Use the copy icon at the top right of the black box.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Open prompt with</div>', unsafe_allow_html=True)

    # Render AI Tools as custom HTML for robust icon loading
    cols = st.columns(4)
    for i, tool in enumerate(AI_TOOLS):
        col = cols[i % 4]
        with col:
            # We use an HTML block with a fallback onerror for the image
            card_html = f"""
            <a href="{tool['url']}" target="_blank" class="ai-card">
                <img src="{tool['icon']}" class="ai-logo" onerror="this.style.display='none'; document.getElementById('fallback-{i}').style.display='flex';">
                <div id="fallback-{i}" class="ai-fallback" style="display:none; background-color: {tool['color']};">{tool['initial']}</div>
                <p class="ai-name">{tool['name']}</p>
            </a>
            """
            st.markdown(card_html, unsafe_allow_html=True)
