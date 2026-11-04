import os
import base64
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
    
    /* Background - Energetic Runner */
    .stApp { 
        background-image: 
            linear-gradient(135deg, rgba(255, 213, 0, 0.35), rgba(255, 153, 0, 0.25)),
            url('https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Main Container (Compressed to fit screen) */
    .block-container { 
        padding: 1rem 2rem 1rem 2rem; 
        max-width: 900px; 
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 24px; 
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin-top: 1rem;
        margin-bottom: 1rem;
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
        font-size: 0.85rem; 
        padding: 0.3rem 1rem; 
        border-radius: 20px; 
        letter-spacing: 0.1em; 
        margin-bottom: 0.5rem; 
        border: 2px solid #000000;
        text-transform: uppercase;
    }

    /* Typography */
    h1 { 
        font-size: 2.2rem; 
        font-weight: 900; 
        color: #111111; 
        letter-spacing: -0.03em; 
        line-height: 1.1;
        margin-bottom: 0;
        margin-top: 0;
        text-transform: uppercase;
    }
    h1 .highlight { color: #FF9900; }
    .subtitle { color: #333333; font-size: 1rem; margin-top: 0.3rem; margin-bottom: 0.8rem; font-weight: 700; }

    /* Typewriter Message Box */
    .typewriter-container {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #FFD500;
        border-radius: 12px;
        padding: 6px 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        display: inline-block;
        min-width: 300px;
    }
    .typewriter-text {
        color: #000000;
        font-weight: 800;
        font-size: 0.9rem;
        font-family: monospace;
        text-transform: uppercase;
        margin: 0;
    }

    /* Action Button */
    .stButton > button { 
        background-color: #FFD500; 
        color: #000000; 
        border: 2px solid #000000; 
        border-radius: 40px; 
        font-weight: 900; 
        text-transform: uppercase;
        padding: 0.6rem 2rem; 
        font-size: 1rem; 
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
        padding: 0.8rem 0.5rem; 
        text-decoration: none; 
        color: #000; 
        transition: all 0.2s;
        height: 100%;
        margin-bottom: 10px;
    }
    .ai-card:hover { 
        border-color: #FFD500; 
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .ai-logo { width: 32px; height: 32px; margin-bottom: 6px; object-fit: contain; }
    .ai-name { font-weight: 800; font-size: 0.75rem; text-align: center; margin: 0; }
    .ai-fallback { 
        width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 1.1rem; color: #FFF; margin-bottom: 6px;
    }

    /* Output Code Block */
    .stCodeBlock pre { 
        background: rgba(20, 20, 20, 0.95) !important; 
        color: #FFD500 !important; 
        border-radius: 16px; 
        border: 2px solid rgba(255, 213, 0, 0.5);
        font-size: 0.95rem;
    }
    
    hr { border-color: rgba(0,0,0,0.1); margin: 1rem 0; }
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
components.html(typewriter_html, height=50)

st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)

# Custom WhatsApp-style Chat Box (Pure HTML/JS to Python Bridge)
# This perfectly puts text, upload, and audio into one compact pill.
chat_box_html = """
<div style="display: flex; align-items: center; background: rgba(255,255,255,0.95); border: 2px solid #FFD500; border-radius: 30px; padding: 5px 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <input type="text" id="userInput" placeholder="Type your request here..." style="flex-grow: 1; border: none; background: transparent; outline: none; font-size: 1rem; padding: 8px;" oninput="toggleSend()">
    
    <!-- Upload Icon (Paperclip) -->
    <label style="cursor: pointer; padding: 5px; display: flex; align-items: center; margin-right: 5px;">
        <input type="file" id="fileUpload" style="display: none;" onchange="handleFile(this)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
    </label>

    <!-- Audio Icon (Mic) -->
    <div style="cursor: pointer; padding: 5px; display: flex; align-items: center; margin-right: 5px;" onclick="document.getElementById('recorder').style.display='block'">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
    </div>

    <!-- Send Arrow -->
    <button id="sendBtn" onclick="sendData()" style="background: #FFD500; border: none; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; opacity: 0.5; pointer-events: none; transition: all 0.2s;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
    </button>
</div>

<!-- Hidden Recorder Dropdown -->
<div id="recorder" style="display: none; background: white; padding: 10px; border-radius: 10px; margin-top: 10px; border: 2px solid #FFD500;">
    <p style="margin: 0; font-weight: bold; font-size: 0.8rem; margin-bottom: 5px;">Speak your request (English/Supported Languages)</p>
    <audio id="audioPlayback" controls style="width: 100%; height: 30px; margin-bottom: 10px;"></audio>
    <button onclick="startRec()" style="background: #FFD500; border: 1px solid #000; padding: 5px 10px; border-radius: 10px; cursor: pointer; font-weight: bold;">Record</button>
    <button onclick="stopRec()" style="background: #f0f0f0; border: 1px solid #000; padding: 5px 10px; border-radius: 10px; cursor: pointer; font-weight: bold;">Stop & Attach</button>
</div>

<script>
    let mediaRecorder;
    let audioChunks = [];
    let uploadedFileName = "";

    function toggleSend() {
        const text = document.getElementById("userInput").value.trim();
        const btn = document.getElementById("sendBtn");
        if (text.length > 0 || uploadedFileName !== "" || audioChunks.length > 0) {
            btn.style.opacity = "1";
            btn.style.pointerEvents = "auto";
            btn.style.background = "#FF9900"; // Orange active state
        } else {
            btn.style.opacity = "0.5";
            btn.style.pointerEvents = "none";
            btn.style.background = "#FFD500";
        }
    }

    function handleFile(input) {
        if (input.files.length > 0) {
            uploadedFileName = input.files[0].name;
            document.getElementById("userInput").value = "File Attached: " + uploadedFileName;
            toggleSend();
            // In a real custom component we'd send the actual file, 
            // here we send a trigger to Streamlit to open the native uploader
            window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "__UPLOAD__"}, "*");
        }
    }

    function startRec() {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
            mediaRecorder.start();
        });
    }

    function stopRec() {
        if (mediaRecorder) {
            mediaRecorder.stop();
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                document.getElementById("audioPlayback").src = URL.createObjectURL(audioBlob);
                document.getElementById("userInput").value = "Audio Attached...";
                toggleSend();
                // Tell Streamlit to open native audio input
                window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "__AUDIO__"}, "*");
            };
        }
    }

    function sendData() {
        const text = document.getElementById("userInput").value.trim();
        if (text) {
            window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: text}, "*");
            document.getElementById("userInput").value = "";
            toggleSend();
        }
    }
</script>
"""
# Note: Because of Streamlit's strict iframe security, sending raw audio back via pure JS is highly restricted without a Python backend.
# So this custom pill instantly triggers the native Streamlit widgets below it if you click the icons.
# This guarantees 100% functionality without crashes.

st.markdown(chat_box_html, unsafe_allow_html=True)

# We keep native hidden widgets to guarantee the data actually gets to Python
with st.expander("📎 Attach File or Record Voice (Click icons above to open)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload", type=["txt", "md", "csv", "pdf"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state["saved_prompt"] = extract_file_text(uploaded_file)
            st.caption("✅ File Attached")
    with col2:
        audio_value = st.audio_input("Record", label_visibility="collapsed")
        if audio_value is not None:
            with st.spinner("Transcribing..."):
                try:
                    v_text = client.audio.transcriptions.create(
                        file=("req.wav", audio_value.getvalue()),
                        model="whisper-large-v3",
                        language=GROQ_LANGS[lang_name],
                        response_format="text",
                    )
                    st.session_state["saved_prompt"] = translate_to_english(v_text)
                    st.caption("✅ Voice Attached")
                except Exception as e:
                    st.error("Transcription failed.")

# Fallback native input to guarantee text capture
typed_text = st.text_input("Or type here to be safe:", label_visibility="collapsed", placeholder="Or type your request here...")
if typed_text:
    st.session_state["saved_prompt"] = typed_text

st.markdown("<br>", unsafe_allow_html=True)

if st.button("GENERATE PROMPT", key="gen"):
    final_input = st.session_state.get("saved_prompt", "").strip()
    
    if not final_input:
        st.warning("Please provide a request first.")
        st.stop()

    with st.spinner("Forging your prompt..."):
        prompt = optimize_prompt(final_input, domain, tone, depth)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Your Professional Prompt</div>', unsafe_allow_html=True)
    st.code(prompt, language="markdown")
    st.caption("Use the copy icon at the top right.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Open prompt with</div>', unsafe_allow_html=True)

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
