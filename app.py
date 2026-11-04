import os
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# ========== API CONFIGURATION ==========
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="Promptline Guru",
    page_icon=None,
    layout="wide"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Global Reset */
    html, body, [class*="css"] {
        font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif;
    }

    /* Main App Background and Layout */
    .stApp {
        display: flex;
        align-items: flex-start;
        justify-content: center;
        background-image:
            linear-gradient(
                135deg,
                rgba(255, 213, 0, 0.35),
                rgba(255, 153, 0, 0.25)
            ),
            url('https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Prevent Content from Being Hidden Behind Streamlit Header */
    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 15vh !important;
        max-width: 750px !important;
        margin: 0 auto !important;
    }

    /* Glassmorphism Container */
    .block-container > div:first-child {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        margin: 0 auto;
        width: 100%;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
    }

    /* App Name Tag */
    .plg-tag {
        display: inline-block;
        background: #FFD500;
        color: #000;
        font-weight: 900;
        font-size: 0.75rem;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        border: 2px solid #000;
        text-transform: uppercase;
    }

    /* Typography */
    h1 {
        font-size: 1.9rem;
        font-weight: 900;
        color: #111;
        line-height: 1.1;
        margin-bottom: 0;
        margin-top: 0;
        text-transform: uppercase;
    }

    h1 .highlight {
        color: #FF9900;
    }

    .subtitle {
        color: #333;
        font-size: 0.85rem;
        margin-top: 0.2rem;
        margin-bottom: 0.8rem;
        font-weight: 700;
    }

    /* Typewriter Box */
    .typewriter-container {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #FFD500;
        border-radius: 8px;
        padding: 4px 10px;
        margin-bottom: 0.8rem;
        display: inline-block;
        min-width: 220px;
    }

    .typewriter-text {
        color: #000;
        font-weight: 800;
        font-size: 0.75rem;
        font-family: monospace;
        text-transform: uppercase;
        margin: 0;
    }

    /* Chat and Audio Alignment */
    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0.5rem !important;
    }

    /* Chat Input */
    [data-testid="stChatInput"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #FFD500 !important;
        border-radius: 30px !important;
        padding: 6px 12px !important;
        min-height: 52px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #FF9900 !important;
    }

    /* Audio Input Container */
    [data-testid="stAudioInput"] {
        width: 56px !important;
        min-width: 56px !important;
        min-height: 56px !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Hide Audio Label */
    [data-testid="stAudioInput"] > div > div:first-child {
        display: none !important;
    }

    /* Audio Recording Button */
    [data-testid="stAudioInput"] button {
        border-radius: 50% !important;
        background: linear-gradient(145deg, #FFE45C, #FFD500) !important;
        border: 2px solid #000 !important;
        width: 52px !important;
        min-width: 52px !important;
        height: 52px !important;
        min-height: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 5px 14px rgba(0,0,0,0.18) !important;
        color: #000 !important;
        margin: 0 !important;
        padding: 0 !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }

    [data-testid="stAudioInput"] button:hover {
        background: linear-gradient(145deg, #FFB700, #FF9900) !important;
        color: #fff !important;
        transform: translateY(-2px) scale(1.04);
        box-shadow: 0 7px 18px rgba(0,0,0,0.22) !important;
    }

    [data-testid="stAudioInput"] button:active {
        transform: scale(0.96);
    }

    [data-testid="stAudioInput"] button:focus-visible {
        outline: 3px solid #FF9900 !important;
        outline-offset: 3px !important;
    }

    [data-testid="stAudioInput"] button svg {
        width: 23px !important;
        height: 23px !important;
    }

    /* Accessibility */
    @media (prefers-reduced-motion: reduce) {
        [data-testid="stAudioInput"] button {
            transition: none !important;
        }
    }

    /* Generate Button */
    .stButton > button {
        background-color: #FFD500;
        color: #000;
        border: 2px solid #000;
        border-radius: 30px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 0.5rem 1.5rem;
        font-size: 0.95rem;
        width: 100%;
        margin-top: 0.8rem;
        height: 48px;
    }

    .stButton > button:hover {
        background-color: #FF9900;
        color: #FFF;
    }

    /* AI Tool Cards */
    .ai-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: rgba(255, 255, 255, 0.97);
        border: 2px solid #E0E0E0;
        border-radius: 14px;
        padding: 1rem 0.5rem;
        text-decoration: none !important;
        color: #000 !important;
        transition: all 0.25s ease;
        height: 100%;
        min-height: 100px;
        margin-bottom: 10px;
    }

    .ai-card:hover {
        border-color: #FFD500;
        transform: translateY(-4px);
        box-shadow: 0 8px 18px rgba(0,0,0,0.12);
    }

    /* AI Brand Logos */
    .ai-logo {
        width: 38px;
        height: 38px;
        margin-bottom: 9px;
        object-fit: contain;
        display: block;
    }

    .ai-name {
        font-weight: 800;
        font-size: 0.75rem;
        text-align: center;
        margin: 0;
        color: #111;
    }

    /* Fallback Logo */
    .ai-fallback {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1rem;
        color: #FFF;
        margin-bottom: 9px;
    }

    /* Output Code Block */
    .stCodeBlock pre {
        background: rgba(20, 20, 20, 0.95) !important;
        color: #FFD500 !important;
        border-radius: 12px;
        border: 2px solid rgba(255, 213, 0, 0.5);
        font-size: 0.8rem;
        padding: 10px !important;
    }

    /* Section Titles */
    .card-title {
        font-size: 1rem;
        font-weight: 900;
        color: #111;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    hr {
        border-color: rgba(0,0,0,0.1);
        margin: 0.8rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ========== DOMAIN SETTINGS ==========
DOMAINS = {
    "General": "General-purpose professional work.",
    "Software Engineering": "Code, architecture, debugging. Emphasize correctness and runnable output.",
    "Business and Strategy": "Strategy, planning, operations. Emphasize measurable objectives.",
    "Education": "Teaching and learning. Emphasize clarity and assessment.",
    "Health": "Health communication. Emphasize accuracy and safety.",
    "Agriculture": "Agricultural extension. Emphasize field-ready guidance.",
    "Government": "Public service delivery. Emphasize clarity and accountability.",
}


# ========== AUDIO LANGUAGES ==========
GROQ_LANGS = {
    "English": "en",
    "Swahili": "sw",
    "French": "fr",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Spanish": "es"
}


# ========== AI PLATFORMS ==========
AI_TOOLS = [
    {
        "name": "ChatGPT",
        "url": "https://chatgpt.com",
        "icon": "https://cdn.simpleicons.org/openai/412991",
        "color": "#412991",
        "initial": "C"
    },
    {
        "name": "Claude",
        "url": "https://claude.ai",
        "icon": "https://cdn.simpleicons.org/anthropic/D97757",
        "color": "#D97757",
        "initial": "C"
    },
    {
        "name": "Gemini",
        "url": "https://gemini.google.com",
        "icon": "https://cdn.simpleicons.org/googlegemini/8E75B2",
        "color": "#8E75B2",
        "initial": "G"
    },
    {
        "name": "Grok",
        "url": "https://grok.com",
        "icon": "https://cdn.simpleicons.org/grok/000000",
        "color": "#000000",
        "initial": "G"
    },
    {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com",
        "icon": "https://cdn.simpleicons.org/deepseek/4D6BFE",
        "color": "#4D6BFE",
        "initial": "D"
    },
    {
        "name": "Copilot",
        "url": "https://copilot.microsoft.com",
        "icon": "https://cdn.simpleicons.org/microsoftcopilot/258FFA",
        "color": "#258FFA",
        "initial": "C"
    },
    {
        "name": "Perplexity",
        "url": "https://www.perplexity.ai",
        "icon": "https://cdn.simpleicons.org/perplexity/20B8CD",
        "color": "#20B8CD",
        "initial": "P"
    }
]


# ========== PROMPT ENGINEERING SYSTEM ==========
META_SYSTEM = """You are a senior prompt engineer. Convert a rough request into a production-ready prompt.
Output ONLY the prompt. Structure: ROLE, OBJECTIVE, CONTEXT AND CONSTRAINTS, INPUTS, PROCESS, OUTPUT FORMAT, QUALITY BAR.
QUALITY BAR must contain concrete, checkable criteria.
Do NOT answer the user's request. Resolve ambiguity with stated defaults."""


def optimize_prompt(user_input, domain, tone, depth):
    system = META_SYSTEM + "\n\nDomain: " + DOMAINS.get(
        domain,
        DOMAINS["General"]
    )

    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": (
                    "Domain: " + domain +
                    "\nTone: " + tone +
                    "\nDepth: " + depth +
                    "\n\nRequest:\n" + user_input
                )
            },
        ],
        temperature=0.4,
        max_tokens=1500,
    )

    return resp.choices[0].message.content


# ========== TRANSLATION FUNCTION ==========
def translate_to_english(text):
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Translate to English. Output only the translation."
            },
            {
                "role": "user",
                "content": text
            },
        ],
        temperature=0.1,
        max_tokens=800,
    )

    return resp.choices[0].message.content.strip()


# ========== FILE EXTRACTION ==========
def extract_file_text(f):
    name = f.name.lower()
    data = f.getvalue()

    if name.endswith(".pdf"):
        import fitz

        doc = fitz.open(stream=data, filetype="pdf")
        extracted_text = "\n".join(
            page.get_text() for page in doc
        )
        doc.close()

        return extracted_text

    return data.decode("utf-8", errors="replace")


# ========== SIDEBAR SETTINGS ==========
with st.sidebar:
    st.markdown(
        "<h2 style='text-align: center;'>Settings</h2>",
        unsafe_allow_html=True
    )

    domain = st.selectbox(
        "Domain",
        list(DOMAINS.keys())
    )

    tone = st.selectbox(
        "Tone",
        ["Professional", "Neutral", "Persuasive", "Instructional"]
    )

    depth = st.selectbox(
        "Depth",
        ["Concise", "Standard", "Detailed", "Exhaustive"],
        index=1
    )

    lang_name = st.selectbox(
        "Audio Language",
        list(GROQ_LANGS.keys()),
        index=0
    )

    st.caption(
        "For Leb Lango, please type instead. Whisper does not support it directly."
    )


# ========== MAIN USER INTERFACE ==========

# Branding
st.markdown(
    '<div class="plg-tag">PROMPTLINE GURU</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<h1>Prompt Better.<br>Build <span class="highlight">Faster.</span></h1>',
    unsafe_allow_html=True
)


# ========== TYPEWRITER COMPONENT ==========
components.html("""
<div class="typewriter-container" style="margin-bottom:0px;">
    <p class="typewriter-text" id="typewriter"></p>
</div>

<script>
    const texts = [
        "Industry-Grade Production Prompt Engineering",
        "A Better Way to Work with Generative AI",
        "Save Time from Frustrating AI Outputs"
    ];

    let c = 0, i = 0, t = "", l = "", d = false;

    (function ty() {
        if (c === texts.length) c = 0;

        t = texts[c];
        l = d ? t.slice(0, --i) : t.slice(0, ++i);

        document.getElementById("typewriter").textContent = l;

        let s = d ? 20 : 60;

        if (!d && l.length === t.length) {
            s = 2000;
            d = true;
        }
        else if (d && l.length === 0) {
            d = false;
            c++;
            s = 500;
        }

        setTimeout(ty, s);
    })();
</script>
""", height=40)


# ========== SUBTITLE ==========
st.markdown(
    '<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>',
    unsafe_allow_html=True
)


# ========== CHAT AND AUDIO INPUT ==========
col1, col2 = st.columns([10, 1])

with col1:
    chat_val = st.chat_input(
        "Type your request here...",
        accept_file=True,
        file_type=["txt", "md", "csv", "pdf"]
    )

    if chat_val:
        if chat_val.text:
            st.session_state["saved_prompt"] = chat_val.text

        if chat_val.files:
            for f in chat_val.files:
                st.session_state["saved_prompt"] = extract_file_text(f)


with col2:
    audio_val = st.audio_input(
        "",
        label_visibility="collapsed"
    )

    if audio_val is not None:
        with st.spinner("Transcribing..."):
            try:
                v_txt = client.audio.transcriptions.create(
                    file=("req.wav", audio_val.getvalue()),
                    model="whisper-large-v3",
                    language=GROQ_LANGS[lang_name],
                    response_format="text",
                )

                st.session_state["saved_prompt"] = translate_to_english(
                    v_txt
                )

                st.toast("Voice captured!")

            except Exception:
                st.error("Mic failed.")


st.markdown("<br>", unsafe_allow_html=True)


# ========== GENERATE PROMPT ==========
if st.button("GENERATE PROMPT", key="gen"):

    final_input = st.session_state.get(
        "saved_prompt",
        ""
    ).strip()

    if not final_input:
        st.warning(
            "Please provide a request (type, upload, or speak)."
        )
        st.stop()

    with st.spinner("Forging your prompt..."):
        prompt = optimize_prompt(
            final_input,
            domain,
            tone,
            depth
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card-title">Your Professional Prompt</div>',
        unsafe_allow_html=True
    )

    st.code(
        prompt,
        language="markdown"
    )

    st.caption(
        "Use the copy icon at the top right of the black box."
    )

    st.markdown("<hr>", unsafe_allow_html=True)


    # ========== OPEN PROMPT WITH AI PLATFORMS ==========
    st.markdown(
        '<div class="card-title">Open prompt with</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    for i, tool in enumerate(AI_TOOLS):
        col = cols[i % 4]

        with col:
            card_html = f"""
            <a href="{tool['url']}"
               target="_blank"
               rel="noopener noreferrer"
               class="ai-card">

                <img
                    src="{tool['icon']}"
                    class="ai-logo"
                    alt="{tool['name']} logo"
                    onerror="
                        this.style.display='none';
                        this.nextElementSibling.style.display='flex';
                    "
                >

                <div
                    class="ai-fallback"
                    style="
                        display:none;
                        background-color:{tool['color']};
                    ">
                    {tool['initial']}
                </div>

                <p class="ai-name">{tool['name']}</p>

            </a>
            """

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )
