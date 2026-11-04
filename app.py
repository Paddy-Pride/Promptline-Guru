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
    /* Global Reset */
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }
    
    /* Centered Background */
    .stApp {
        display: flex;
        align-items: center;
        justify-content: center;
        background-image: 
            linear-gradient(135deg, rgba(255, 213, 0, 0.25), rgba(255, 153, 0, 0.15)),
            url('https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .block-container { 
        padding-top: 2vh !important; 
        padding-bottom: 10vh !important; 
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    
    /* Beautiful Glassmorphism Container */
    .block-container > div:first-child { 
        padding: 2.5rem; 
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 24px; 
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
        margin: 0 auto;
        width: 100%;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); }

    /* App Name Tag */
    .plg-tag { 
        display: inline-block; background: #FFD500; color: #000; 
        font-weight: 900; font-size: 0.8rem; padding: 0.3rem 1rem; 
        border-radius: 20px; letter-spacing: 0.1em; margin-bottom: 0.8rem; 
        border: 2px solid #000; text-transform: uppercase;
    }

    /* Typography */
    h1 { font-size: 2.4rem; font-weight: 900; color: #111; line-height: 1.1; margin-bottom: 0; margin-top: 0; text-transform: uppercase; }
    h1 .highlight { color: #FF9900; }
    .subtitle { color: #333; font-size: 1rem; margin-top: 0.3rem; margin-bottom: 1.2rem; font-weight: 700; }

    /* Typewriter Box (Fitted perfectly) */
    .typewriter-container {
        background: rgba(255, 255, 255, 0.9); border: 2px solid #FFD500;
        border-radius: 12px; padding: 8px 15px; margin-bottom: 1rem;
        display: block; width: fit-content; min-width: 100%; box-sizing: border-box;
    }
    .typewriter-text { color: #000; font-weight: 800; font-size: 0.85rem; font-family: monospace; text-transform: uppercase; margin: 0; }

    /* --- CUSTOM CHAT BAR HTML/CSS --- */
    .custom-chat-bar {
        display: flex;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #FFD500;
        border-radius: 30px;
        padding: 6px 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: 56px;
        margin-bottom: 1rem;
    }
    
    .chat-input {
        flex-grow: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 1rem;
        color: #000;
        font-family: inherit;
    }
    
    .chat-icon-btn {
        background: transparent;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 6px;
        color: #333;
        padding: 5px;
        border-radius: 50%;
        transition: background 0.2s;
    }
    .chat-icon-btn:hover { background: #f0f0f0; }
    
    .chat-mic-btn {
        background-color: #FFD500;
        border: 2px solid #000;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin-left: 5px;
        transition: all 0.2s;
    }
    .chat-mic-btn:hover { background-color: #FF9900; color: #fff; }

    /* Generate Button */
    .stButton > button { 
        background-color: #FFD500; color: #000; border: 2px solid #000; 
        border-radius: 30px; font-weight: 900; text-transform: uppercase;
        padding: 0.6rem 1.5rem; font-size: 1rem; width: 100%; margin-top: 0.5rem;
        height: 50px;
    }
    .stButton > button:hover { background-color: #FF9900; color: #FFF; }
    
    /* AI Tool Cards Grid */
    .ai-card { 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background-color: rgba(255, 255, 255, 0.95); border: 2px solid #E0E0E0; 
        border-radius: 12px; padding: 0.6rem 0.3rem; text-decoration: none; color: #000; 
        transition: all 0.2s; height: 100%; margin-bottom: 8px;
    }
    .ai-card:hover { border-color: #FFD500; transform: translateY(-2px); }
    .ai-logo { width: 26px; height: 26px; margin-bottom: 6px; object-fit: contain; }
    .ai-name { font-weight: 800; font-size: 0.7rem; text-align: center; margin: 0; }
    .ai-fallback { 
        width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 0.95rem; color: #FFF; margin-bottom: 6px;
    }

    /* Output Code Block */
    .stCodeBlock pre { 
        background: rgba(20, 20, 20, 0.95) !important; color: #FFD500 !important; 
        border-radius: 12px; border: 2px solid rgba(255, 213, 0, 0.5); font-size: 0.85rem;
        padding: 12px !important;
    }
    hr { border-color: rgba(0,0,0,0.1); margin: 1rem 0; }
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
    {"name": "ChatGPT", "url": "https://chat.openai.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/openai-color.png", "color": "#10A37F", "initial": "C"},
    {"name": "Claude", "url": "https://claude.ai", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/claude-color.png", "color": "#D97757", "initial": "C"},
    {"name": "Gemini", "url": "https://gemini.google.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/gemini-color.png", "color": "#4285F4", "initial": "G"},
    {"name": "Grok", "url": "https://grok.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/grok-color.png", "color": "#000000", "initial": "G"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/deepseek-color.png", "color": "#4D6BFE", "initial": "D"},
    {"name": "Copilot", "url": "https://copilot.microsoft.com", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/copilot-color.png", "color": "#0078D4", "initial": "C"},
    {"name": "Perplexity", "url": "https://www.perplexity.ai", "icon": "https://unpkg.com/@lobehub/icons-static-png@latest/color/perplexity-color.png", "color": "#20808D", "initial": "P"},
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
    domain = st.selectbox("Domain", list(DOMAINS.keys()))
    tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"])
    depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)
    lang_name = st.selectbox("Audio Language", list(GROQ_LANGS.keys()), index=0)
    st.caption("For Leb Lango, please type instead. Whisper does not support it directly.")

# ========== UI Main ==========
st.markdown('<div class="plg-tag">PROMPTLINE GURU</div>', unsafe_allow_html=True)
st.markdown('<h1>Prompt Better.<br>Build <span class="highlight">Faster.</span></h1>', unsafe_allow_html=True)

# Typewriter Component
components.html("""
<div class="typewriter-container" style="margin-bottom:0px;"><p class="typewriter-text" id="typewriter"></p></div>
<script>
    const texts = ["Industry-Grade Production Prompt Engineering", "A Better Way to Work with Generative AI", "Save Time from Frustrating AI Outputs"];
    let c = 0, i = 0, t = "", l = "", d = false;
    (function ty() {
        if (c === texts.length) c = 0;
        t = texts[c];
        l = d ? t.slice(0, --i) : t.slice(0, ++i);
        document.getElementById("typewriter").textContent = l;
        let s = d ? 20 : 60;
        if (!d && l.length === t.length) { s = 2000; d = true; } 
        else if (d && l.length === 0) { d = false; c++; s = 500; }
        setTimeout(ty, s);
    })();
</script>
""", height=45)

st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)

# --- CUSTOM CHAT BAR VISUAL (Fake input that passes data via JS) ---
st.markdown("""
<div class="custom-chat-bar">
    <button class="chat-icon-btn" onclick="document.getElementById('file-upload').click()">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
    </button>
    
    <input type="text" class="chat-input" id="promptInput" placeholder="Type your request here..." onkeypress="handleEnter(event)">
    
    <button class="chat-icon-btn" onclick="document.getElementById('mic-trigger').click()">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
    </button>
    
    <button class="chat-mic-btn" onclick="submitPrompt()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
    </button>
</div>

<!-- Hidden native inputs to make it work perfectly -->
<div style="display:none;">
    <div id="file-upload">%s</div>
    <div id="mic-trigger">%s</div>
</div>

<script>
    function handleEnter(e) {
        if (e.key === "Enter") submitPrompt();
    }
    function submitPrompt() {
        const val = document.getElementById("promptInput").value;
        if (val.trim() !== "") {
            // Send to Streamlit hidden input
            window.parent.postMessage({
                isStreamlitMessage: true,
                type: "streamlit:setComponentValue",
                value: val
            }, "*");
            document.getElementById("promptInput").value = "";
        }
    }
</script>
""" % ("", ""), unsafe_allow_html=True)

# --- NATIVE HIDDEN INPUTS (For actual data capture) ---
# We use Streamlit's native elements but style them to sit underneath in an expander so they don't break the UI.
with st.expander("Or use native inputs (if icons above don't work)", expanded=False):
    typed = st.text_input("Type here", placeholder="Type here and press Enter...", label_visibility="collapsed")
    if typed:
        st.session_state["saved_prompt"] = typed
        
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload File", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state["saved_prompt"] = extract_file_text(uploaded_file)
            st.caption("File uploaded.")
    with col2:
        audio_val = st.audio_input("Record", label_visibility="collapsed")
        if audio_val is not None:
            with st.spinner("Transcribing..."):
                try:
                    v_txt = client.audio.transcriptions.create(
                        file=("req.wav", audio_val.getvalue()),
                        model="whisper-large-v3",
                        language=GROQ_LANGS[lang_name],
                        response_format="text",
                    )
                    st.session_state["saved_prompt"] = translate_to_english(v_txt)
                    st.caption("Voice captured.")
                except Exception as e:
                    st.error("Mic failed.")

st.markdown("<br>", unsafe_allow_html=True)

# --- GENERATION LOGIC ---
if st.button("GENERATE PROMPT", key="gen"):
    final_input = st.session_state.get("saved_prompt", "").strip()
    
    if not final_input:
        st.warning("Please provide a request (type, upload, or speak).")
        st.stop()

    with st.spinner("Forging your prompt..."):
        prompt = optimize_prompt(final_input, domain, tone, depth)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Professional Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Use the copy icon at the top right of the black box.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Open prompt with</div>', unsafe_allow_html=True)

    # AI Logos with Color and Fallback
    cols = st.columns(4)
    for i, tool in enumerate(AI_TOOLS):
        col = cols[i % 4]
        with col:
            card_html = f"""
            <a href="{tool['url']}" target="_blank" class="ai-card">
                <img src="{tool['icon']}" class="ai-logo" onerror="this.style.display='none'; document.getElementById('fallback-{i}').style.display='flex';">
                <div id="fallback-{i}" class="ai-fallback" style="display:none; background-color: {tool['color']};">{tool['initial']}</div>
                <p class="ai-name">{tool['name']}</p>
            </a>
            """
            st.markdown(card_html, unsafe_allow_html=True)
