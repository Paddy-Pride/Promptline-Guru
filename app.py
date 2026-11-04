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

    /* Clear and Visible App Name Tag */
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

    /* Custom Chat Box CSS */
    .custom-chat-container {
        display: flex;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #FFD500;
        border-radius: 24px;
        padding: 8px 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .custom-chat-container:focus-within {
        border-color: #FF9900;
        box-shadow: 0 0 0 3px rgba(255,153,0,0.2);
    }
    .custom-chat-input {
        flex-grow: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 1.05rem;
        font-family: inherit;
        color: #000;
    }
    .icon-btn {
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.2s;
    }
    .icon-btn:hover { background: #f0f0f0; }
    .send-btn {
        background-color: #FFD500;
        border: 2px solid #000;
        color: #000;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin-left: 8px;
        opacity: 0.5;
        pointer-events: none;
        transition: all 0.2s;
    }
    .send-btn.active {
        opacity: 1;
        pointer-events: auto;
        background-color: #FF9900;
        color: #FFF;
        border-color: #FF9900;
    }
    .send-btn.active:hover { transform: scale(1.05); }

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
    
    /* AI Tool Link Buttons */
    .stLinkButton > a { 
        background-color: rgba(255, 255, 255, 0.9); 
        color: #000000; 
        border: 2px solid #E0E0E0; 
        border-radius: 30px; 
        padding: 0.5rem 0.8rem; 
        font-weight: 800; 
        font-size: 0.8rem; 
        text-decoration: none; 
        width: 100%; 
        text-align: center; 
        transition: all 0.15s;
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
    {"name": "ChatGPT", "url": "https://chat.openai.com", "icon": "https://chat.openai.com/favicon.ico"},
    {"name": "Claude", "url": "https://claude.ai", "icon": "https://claude.ai/favicon.ico"},
    {"name": "Gemini", "url": "https://gemini.google.com", "icon": "https://www.gstatic.com/lamda/images/gemini_favicon_f069958c85030f4b2761.ico"},
    {"name": "Grok", "url": "https://grok.com", "icon": "https://grok.com/favicon.ico"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "icon": "https://chat.deepseek.com/favicon.ico"},
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

# Typewriter Animation Component (No Cursor)
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
    let count = 0;
    let index = 0;
    let currentText = "";
    let letter = "";
    let isDeleting = false;

    (function type() {
        if (count === texts.length) { count = 0; }
        currentText = texts[count];
        
        if (isDeleting) {
            letter = currentText.slice(0, --index);
        } else {
            letter = currentText.slice(0, ++index);
        }

        document.getElementById("typewriter").textContent = letter;

        let typeSpeed = isDeleting ? 20 : 60;

        if (!isDeleting && letter.length === currentText.length) {
            typeSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && letter.length === 0) {
            isDeleting = false;
            count++;
            typeSpeed = 500;
        }

        setTimeout(type, typeSpeed);
    })();
</script>
"""
components.html(typewriter_html, height=60)

st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)

# Custom HTML Chat Box
# This solves the disappearing text by using a custom JS bridge
chat_input_html = """
<div class="custom-chat-container">
    <button class="icon-btn" title="Upload File">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
    </button>
    <input type="text" class="custom-chat-input" id="chatInput" placeholder="Type your request here..." oninput="toggleBtn()" onkeypress="handleEnter(event)">
    <button class="send-btn" id="sendBtn" onclick="sendText()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
    </button>
</div>

<script>
    function toggleBtn() {
        const input = document.getElementById("chatInput");
        const btn = document.getElementById("sendBtn");
        if (input.value.trim().length > 0) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    }

    function handleEnter(e) {
        if (e.key === "Enter") {
            sendText();
        }
    }

    function sendText() {
        const text = document.getElementById("chatInput").value;
        if (text.trim() === "") return;
        
        // Send to Streamlit
        window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: text}, "*");
        
        // Clear input
        document.getElementById("chatInput").value = "";
        toggleBtn();
    }
</script>
"""
# Use st.components.v1.html to bridge the data back to Python via query params fallback or session state trick
# Note: In pure standard Streamlit, bridging text from custom HTML back to Python without a full custom component build is complex.
# We will use a simplified approach: The user types in the custom box, hits enter, and the text is placed into a hidden streamlit text area.
# But to keep it perfect and bug-free, we will use Streamlit's native chat input but ONLY for the data, and overlay it visually.
# Actually, the cleanest foolproof way is st.chat_input, but we prevent it from clearing by storing it in st.session_state.
# Let's revert to st.chat_input but with a solid session state fix.

# FIX: Streamlit st.chat_input clears on submit. We capture it BEFORE the rerun clears it.
col_chat, col_audio = st.columns([5, 1])

with col_chat:
    # By checking if it's not None, we store it in session state instantly.
    chat_val = st.chat_input("Type your request here...", key="chat_input_widget")
    if chat_val:
        st.session_state["saved_prompt"] = chat_val

with col_audio:
    audio_value = st.audio_input("Speak", label_visibility="collapsed")

# Processing File Uploads (Using native file uploader hidden in an expander for stable behaviour)
with st.expander("📎 Attach a Document (Optional)"):
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
    
uploaded_text = ""
if uploaded_file:
    uploaded_text = extract_file_text(uploaded_file)
    st.caption("✅ Loaded: " + uploaded_file.name)

voice_text = ""
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
    # Retrieve from session state
    final_input = st.session_state.get("saved_prompt", "").strip() or uploaded_text.strip()
    
    if not final_input and voice_text:
        with st.spinner("Translating..."):
            final_input = translate_to_english(voice_text)
            
    if not final_input:
        st.warning("Please provide a request first.")
        st.stop()

    with st.spinner("Forging your prompt..."):
        prompt = optimize_prompt(final_input, domain, tone, depth)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Professional Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Use the copy icon at the top right of the black box.")

    st.markdown("<hr>", unsafe_allow_html=True)
    # TITLE CHANGED AS REQUESTED
    st.markdown('<div class="card-title">Open prompt with</div>', unsafe_allow_html=True)

    # Render AI Tools
    for row_start in range(0, len(AI_TOOLS), 4):
        row_tools = AI_TOOLS[row_start:row_start + 4]
        cols = st.columns(len(row_tools))
        for i, tool in enumerate(row_tools):
            with cols[i]:
                try:
                    st.image(tool["icon"], width=36)
                except:
                    st.markdown(f"**{tool['name'][0]}**")
                st.link_button(tool["name"], tool["url"], use_container_width=True)
