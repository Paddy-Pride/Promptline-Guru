
import os
import html
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Promptline Guru",
    page_icon=None,
    layout="wide"
)


# =========================================================
# GROQ API CONFIGURATION
# =========================================================

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is missing. Add it to your Streamlit "
        "Cloud secrets or environment variables."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


# =========================================================
# DOMAIN SETTINGS
# =========================================================

DOMAINS = {
    "General": "General-purpose professional work.",
    "Software Engineering": (
        "Code, architecture, debugging. "
        "Emphasize correctness and runnable output."
    ),
    "Business and Strategy": (
        "Strategy, planning, operations. "
        "Emphasize measurable objectives."
    ),
    "Education": (
        "Teaching and learning. "
        "Emphasize clarity and assessment."
    ),
    "Health": (
        "Health communication. Emphasize accuracy and safety."
    ),
    "Agriculture": (
        "Agricultural extension. Emphasize field-ready guidance."
    ),
    "Government": (
        "Public service delivery. Emphasize clarity and accountability."
    ),
}


# =========================================================
# AUDIO LANGUAGE SETTINGS
# =========================================================

GROQ_LANGS = {
    "English": "en",
    "Swahili": "sw",
    "French": "fr",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Spanish": "es"
}


# =========================================================
# AI TOOLS AND FULL-COLOUR LOGOS
# =========================================================

AI_TOOLS = [
    {
        "name": "ChatGPT",
        "url": "https://chatgpt.com/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/openai-color.png"
        ),
        "color": "#10A37F",
        "initial": "C"
    },
    {
        "name": "Claude",
        "url": "https://claude.ai/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/claude-color.png"
        ),
        "color": "#D97757",
        "initial": "C"
    },
    {
        "name": "Gemini",
        "url": "https://gemini.google.com/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/gemini-color.png"
        ),
        "color": "#4285F4",
        "initial": "G"
    },
    {
        "name": "Grok",
        "url": "https://grok.com/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/grok-color.png"
        ),
        "color": "#000000",
        "initial": "G"
    },
    {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/deepseek-color.png"
        ),
        "color": "#4D6BFE",
        "initial": "D"
    },
    {
        "name": "Copilot",
        "url": "https://copilot.microsoft.com/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/copilot-color.png"
        ),
        "color": "#0078D4",
        "initial": "C"
    },
    {
        "name": "Perplexity",
        "url": "https://www.perplexity.ai/",
        "icon": (
            "https://unpkg.com/@lobehub/icons-static-png@latest/"
            "color/perplexity-color.png"
        ),
        "color": "#20808D",
        "initial": "P"
    }
]


# =========================================================
# PROMPT ENGINEERING SYSTEM
# =========================================================

META_SYSTEM = """
You are a senior prompt engineer.

Convert a rough request into a production-ready prompt.

Output ONLY the prompt.

Structure:

ROLE
OBJECTIVE
CONTEXT AND CONSTRAINTS
INPUTS
PROCESS
OUTPUT FORMAT
QUALITY BAR

QUALITY BAR must contain concrete, checkable criteria.

Do NOT answer the user's request.

Resolve ambiguity with stated defaults.
"""


# =========================================================
# PROMPT OPTIMIZATION FUNCTION
# =========================================================

def optimize_prompt(user_input, domain, tone, depth):

    system = (
        META_SYSTEM
        + "\n\nDomain: "
        + DOMAINS.get(domain, DOMAINS["General"])
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": (
                    "Domain: " + domain
                    + "\nTone: " + tone
                    + "\nDepth: " + depth
                    + "\n\nRequest:\n" + user_input
                )
            }
        ],

        temperature=0.4,
        max_tokens=1500
    )

    return response.choices[0].message.content


# =========================================================
# TRANSLATION FUNCTION
# =========================================================

def translate_to_english(text):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "Translate to English. "
                    "Output only the translation."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],

        temperature=0.1,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()


# =========================================================
# FILE TEXT EXTRACTION
# =========================================================

def extract_file_text(uploaded_file):

    filename = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if filename.endswith(".pdf"):

        import fitz

        document = fitz.open(
            stream=data,
            filetype="pdf"
        )

        extracted_text = "\n".join(
            page.get_text()
            for page in document
        )

        document.close()

        return extracted_text

    return data.decode(
        "utf-8",
        errors="replace"
    )


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* GLOBAL FONT */

    html, body, [class*="css"] {
        font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif;
    }

    /* BACKGROUND */

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
            url(
                'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop'
            );

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* PREVENT BRANDING FROM HIDING BEHIND STREAMLIT HEADER */

    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 15vh !important;
        max-width: 750px !important;
        margin: 0 auto !important;
    }

    /* GLASS CONTAINER */

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

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
    }

    /* BRANDING TAG */

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

    /* MAIN HEADING */

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

    /* TYPEWRITER BOX */

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

    /* CHAT AND AUDIO ALIGNMENT */

    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0.5rem !important;
    }

    /* CHAT INPUT */

    [data-testid="stChatInput"] {
        background-color: rgba(255, 255, 255, 0.95) !important;

        border: 2px solid #FFD500 !important;
        border-radius: 30px !important;

        padding: 6px 12px !important;
        min-height: 52px !important;

        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #FF9900 !important;
    }

    /* AUDIO INPUT */

    [data-testid="stAudioInput"] {
        width: 56px !important;
        min-width: 56px !important;

        min-height: 56px !important;

        margin: 0 !important;
        padding: 2px !important;

        overflow: visible !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stAudioInput"] > div > div:first-child {
        display: none !important;
    }

    [data-testid="stAudioInput"] button {
        width: 52px !important;
        min-width: 52px !important;

        height: 52px !important;
        min-height: 52px !important;

        border-radius: 50% !important;

        background: linear-gradient(
            145deg,
            #FFE45C,
            #FFD500
        ) !important;

        border: 2px solid #171717 !important;
        color: #111 !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        margin: 0 !important;
        padding: 0 !important;

        box-shadow:
            0 5px 14px rgba(0, 0, 0, 0.16),
            inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;

        transition:
            transform 160ms ease,
            background 160ms ease,
            box-shadow 160ms ease !important;
    }

    [data-testid="stAudioInput"] button:hover {
        background: linear-gradient(
            145deg,
            #FFB52E,
            #FF9900
        ) !important;

        color: #fff !important;
        transform: translateY(-2px);

        box-shadow:
            0 7px 18px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stAudioInput"] button:focus-visible {
        outline: 3px solid #111 !important;
        outline-offset: 3px !important;
    }

    [data-testid="stAudioInput"] button:active {
        transform: scale(0.96);
    }

    [data-testid="stAudioInput"] button svg {
        width: 22px !important;
        height: 22px !important;
        stroke-width: 2.2px !important;
    }

    @media (prefers-reduced-motion: reduce) {
        [data-testid="stAudioInput"] button {
            transition: none !important;
        }
    }

    /* GENERATE BUTTON */

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

    /* OUTPUT CODE BLOCK */

    .stCodeBlock pre {
        background: rgba(20, 20, 20, 0.95) !important;
        color: #FFD500 !important;

        border-radius: 12px;
        border: 2px solid rgba(255, 213, 0, 0.5);

        font-size: 0.8rem;
        padding: 10px !important;
    }

    /* SECTION TITLES */

    .card-title {
        font-size: 1rem;
        font-weight: 900;
        color: #111;
        margin: 0.5rem 0;
    }

    hr {
        border-color: rgba(0, 0, 0, 0.1);
        margin: 0.8rem 0;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR SETTINGS
# =========================================================

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
        [
            "Professional",
            "Neutral",
            "Persuasive",
            "Instructional"
        ]
    )

    depth = st.selectbox(
        "Depth",
        [
            "Concise",
            "Standard",
            "Detailed",
            "Exhaustive"
        ],
        index=1
    )

    lang_name = st.selectbox(
        "Audio Language",
        list(GROQ_LANGS.keys()),
        index=0
    )

    st.caption(
        "For Leb Lango, please type instead. "
        "Whisper does not support it directly."
    )


# =========================================================
# MAIN INTERFACE
# =========================================================

st.markdown(
    '<div class="plg-tag">PROMPTLINE GURU</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<h1>Prompt Better.<br>Build '
    '<span class="highlight">Faster.</span></h1>',
    unsafe_allow_html=True
)


# =========================================================
# TYPEWRITER COMPONENT
# =========================================================

components.html("""
<div class="typewriter-container"
     style="margin-bottom:0px;">

    <p class="typewriter-text"
       id="typewriter"></p>

</div>

<style>
    .typewriter-container {
        background: rgba(255,255,255,0.95);
        border: 2px solid #FFD500;
        border-radius: 8px;
        padding: 4px 10px;
        display: inline-block;
        min-width: 220px;
    }

    .typewriter-text {
        color: #000;
        font-weight: 800;
        font-size: 12px;
        font-family: monospace;
        text-transform: uppercase;
        margin: 0;
    }
</style>

<script>

    const texts = [
        "Industry-Grade Production Prompt Engineering",
        "A Better Way to Work with Generative AI",
        "Save Time from Frustrating AI Outputs"
    ];

    let c = 0;
    let i = 0;
    let t = "";
    let l = "";
    let d = false;

    (function ty() {

        if (c === texts.length) {
            c = 0;
        }

        t = texts[c];

        l = d
            ? t.slice(0, --i)
            : t.slice(0, ++i);

        document.getElementById(
            "typewriter"
        ).textContent = l;

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


st.markdown(
    '<div class="subtitle">'
    'Type, upload, or speak. Instantly generate '
    'professional-grade AI prompts.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHAT INPUT AND AUDIO INPUT
# =========================================================

col1, col2 = st.columns([10, 1])


with col1:

    chat_val = st.chat_input(
        "Type your request here...",
        accept_file=True,
        file_type=[
            "txt",
            "md",
            "csv",
            "pdf"
        ]
    )

    if chat_val:

        if chat_val.text:
            st.session_state["saved_prompt"] = chat_val.text

        if chat_val.files:

            for uploaded_file in chat_val.files:

                st.session_state["saved_prompt"] = (
                    extract_file_text(uploaded_file)
                )


with col2:

    audio_val = st.audio_input(
        "",
        label_visibility="collapsed"
    )

    if audio_val is not None:

        with st.spinner("Transcribing..."):

            try:

                voice_text = client.audio.transcriptions.create(
                    file=(
                        "req.wav",
                        audio_val.getvalue()
                    ),

                    model="whisper-large-v3",

                    language=GROQ_LANGS[lang_name],

                    response_format="text"
                )

                st.session_state["saved_prompt"] = (
                    translate_to_english(voice_text)
                )

                st.toast("Voice captured!")

            except Exception:
                st.error(
                    "Mic failed. Please try again or type your request."
                )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =========================================================
# GENERATE PROMPT
# =========================================================

if st.button(
    "GENERATE PROMPT",
    key="gen"
):

    final_input = st.session_state.get(
        "saved_prompt",
        ""
    ).strip()

    if not final_input:

        st.warning(
            "Please provide a request "
            "(type, upload, or speak)."
        )

        st.stop()

    try:

        with st.spinner("Forging your prompt..."):

            prompt = optimize_prompt(
                final_input,
                domain,
                tone,
                depth
            )

        # ---------------------------------------------
        # GENERATED PROMPT
        # ---------------------------------------------

        st.markdown(
            "<hr>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">'
            'Your Professional Prompt'
            '</div>',
            unsafe_allow_html=True
        )

        st.code(
            prompt,
            language="markdown"
        )

        st.caption(
            "Use the copy icon at the top right of the black box."
        )

        # ---------------------------------------------
        # OPEN WITH AI TOOLS
        # ---------------------------------------------

        st.markdown(
            "<hr>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">'
            'Open prompt with'
            '</div>',
            unsafe_allow_html=True
        )

        # Build the cards using HTML.
        # components.html renders this inside an iframe,
        # preventing Streamlit from displaying the HTML as text.

        ai_cards = ""

        for tool in AI_TOOLS:

            name = html.escape(tool["name"])
            url = html.escape(tool["url"], quote=True)
            icon = html.escape(tool["icon"], quote=True)
            color = html.escape(tool["color"], quote=True)
            initial = html.escape(tool["initial"])

            ai_cards += f"""
                <a
                    class="ai-card"
                    href="{url}"
                    target="_blank"
                    rel="noopener noreferrer"
                >

                    <img
                        class="ai-logo"
                        src="{icon}"
                        alt="{name} logo"
                        onerror="
                            this.style.display='none';
                            this.nextElementSibling.style.display='flex';
                        "
                    >

                    <div
                        class="ai-fallback"
                        style="
                            display:none;
                            background-color:{color};
                            color:#ffffff;
                        "
                    >
                        {initial}
                    </div>

                    <p class="ai-name">
                        {name}
                    </p>

                </a>
            """

        ai_html = f"""
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">

            <style>

                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    padding: 5px;
                    background: transparent;
                    font-family: Arial, Helvetica, sans-serif;
                }}

                .ai-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                    gap: 12px;
                    width: 100%;
                }}

                .ai-card {{
                    min-height: 110px;
                    padding: 12px 5px;

                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;

                    background: rgba(255,255,255,0.97);
                    border: 2px solid #E0E0E0;
                    border-radius: 14px;

                    text-decoration: none;
                    color: #222222;

                    transition: all 0.2s ease;
                }}

                .ai-card:hover {{
                    border-color: #FFD500;
                    transform: translateY(-4px);
                    box-shadow: 0 5px 14px rgba(0,0,0,0.10);
                }}

                .ai-logo {{
                    width: 42px;
                    height: 42px;
                    object-fit: contain;
                    display: block;
                    margin-bottom: 9px;
                }}

                .ai-fallback {{
                    width: 42px;
                    height: 42px;
                    border-radius: 50%;

                    align-items: center;
                    justify-content: center;

                    font-size: 20px;
                    font-weight: bold;

                    margin-bottom: 9px;
                }}

                .ai-name {{
                    font-size: 12px;
                    font-weight: 800;
                    text-align: center;
                    margin: 0;
                    color: #222222;
                }}

                @media (max-width: 500px) {{

                    .ai-grid {{
                        grid-template-columns: repeat(2, minmax(0, 1fr));
                    }}

                }}

            </style>

        </head>

        <body>

            <div class="ai-grid">

                {ai_cards}

            </div>

        </body>

        </html>
        """

        components.html(
            ai_html,
            height=260,
            scrolling=False
        )

    except Exception:
        st.error(
            "Something went wrong while generating your prompt. "
            "Please check your Groq API configuration and try again."
        )
        st.exception(Exception)
