import os
import html
import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="Promptline Guru",
    page_icon=None,
    layout="wide"
)

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error(
        "Groq API key is missing. Add GROQ_API_KEY to your "
        "Streamlit secrets or environment variables."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


AI_TOOLS = [
    {"name": "ChatGPT", "url": "https://chatgpt.com/", "icon": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg", "color": "#10A37F", "initial": "C"},
    {"name": "Claude", "url": "https://claude.ai/", "icon": "https://cdn.simpleicons.org/claude/D97757", "color": "#D97757", "initial": "C"},
    {"name": "Gemini", "url": "https://gemini.google.com/", "icon": "https://cdn.simpleicons.org/googlegemini/8E75B2", "color": "#8E75B2", "initial": "G"},
    {"name": "Grok", "url": "https://grok.com/", "icon": "https://cdn.simpleicons.org/x/000000", "color": "#000000", "initial": "G"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com/", "icon": "https://cdn.simpleicons.org/deepseek/4D6BFE", "color": "#4D6BFE", "initial": "D"},
    {"name": "Copilot", "url": "https://copilot.microsoft.com/", "icon": "https://cdn.simpleicons.org/githubcopilot/258FFA", "color": "#258FFA", "initial": "C"},
    {"name": "Perplexity", "url": "https://www.perplexity.ai/", "icon": "https://cdn.simpleicons.org/perplexity/20B8CD", "color": "#20B8CD", "initial": "P"},
    {"name": "Mistral", "url": "https://chat.mistral.ai/", "icon": "https://cdn.simpleicons.org/mistralai/FF7000", "color": "#FF7000", "initial": "M"},
    {"name": "Hugging Face", "url": "https://huggingface.co/chat/", "icon": "https://cdn.simpleicons.org/huggingface/FFD21E", "color": "#FFD21E", "initial": "H"},
    {"name": "Poe", "url": "https://poe.com/", "icon": "https://cdn.simpleicons.org/poe/5D5CDE", "color": "#5D5CDE", "initial": "P"},
    {"name": "Meta AI", "url": "https://www.meta.ai/", "icon": "https://registry.npmmirror.com/@lobehub/icons-static-svg/latest/files/icons/meta-color.svg", "color": "#0064E0", "initial": "M"},
    {"name": "Sunbird AI", "url": "https://sunbird.ai/", "icon": "https://cdn.brandfetch.io/sunbird.ai/w/400/h/400", "color": "#D85037", "initial": "S"},
]


DOMAINS = {
    "General": "General-purpose professional work.",
    "Software Engineering": "Code, architecture, debugging. Emphasize correctness and runnable output.",
    "Business and Strategy": "Strategy, planning, operations. Emphasize measurable objectives.",
    "Education": "Teaching and learning. Emphasize clarity and assessment.",
    "Health": "Health communication. Emphasize accuracy and safety.",
    "Agriculture": "Agricultural extension. Emphasize field-ready guidance.",
    "Government": "Public service delivery. Emphasize clarity and accountability.",
}

GROQ_LANGS = {
    "English": "en", "Swahili": "sw", "French": "fr",
    "Arabic": "ar", "Portuguese": "pt", "Spanish": "es"
}


st.markdown("""
<style>
    html, body, [class*="css"] { font-family: Arial, Helvetica, "Segoe UI", Roboto, sans-serif; }

    .stApp {
        display: flex; align-items: flex-start; justify-content: center;
        background-image: linear-gradient(135deg, rgba(255,213,0,0.35), rgba(255,153,0,0.25)),
            url('https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 15vh !important;
        max-width: 750px !important;
        margin: 0 auto !important;
    }

    .block-container > div:first-child {
        padding: 2rem; background: rgba(255,255,255,0.7);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border-radius: 20px; border: 1px solid rgba(255,255,255,0.9);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15); margin: 0 auto; width: 100%;
    }

    [data-testid="stSidebar"] { background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); }

    .plg-tag {
        display: inline-block; background: #FFD500; color: #000; font-weight: 900; font-size: 0.75rem;
        padding: 0.25rem 0.8rem; border-radius: 20px; letter-spacing: 0.1em;
        margin-bottom: 0.5rem; border: 2px solid #000; text-transform: uppercase;
    }

    h1 { font-size: 1.9rem; font-weight: 900; color: #111; line-height: 1.1; margin: 0; text-transform: uppercase; }
    h1 .highlight { color: #FF9900; }
    .subtitle { color: #333; font-size: 0.85rem; margin: 0.2rem 0 0.8rem; font-weight: 700; }

    div[data-testid="stHorizontalBlock"] { align-items: center !important; gap: 0.5rem !important; }

    [data-testid="stChatInput"] {
        background-color: rgba(255,255,255,0.95) !important;
        border: 2px solid #FFD500 !important; border-radius: 30px !important;
        padding: 6px 12px !important; min-height: 52px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    [data-testid="stChatInput"]:focus-within { border-color: #FF9900 !important; }

    [data-testid="stAudioInput"] button {
        width: 52px !important; height: 52px !important; border-radius: 50% !important;
        background: linear-gradient(145deg, #FFE45C, #FFD500) !important;
        border: 2px solid #171717 !important; color: #111 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        padding: 0 !important; box-shadow: 0 5px 14px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.7) !important;
        transition: transform 160ms ease, background 160ms ease, box-shadow 160ms ease !important;
    }

    [data-testid="stAudioInput"] button:hover {
        background: linear-gradient(145deg, #FFB52E, #FF9900) !important;
        color: #fff !important; transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(0,0,0,0.2) !important;
    }

    [data-testid="stAudioInput"] button svg { width: 22px !important; height: 22px !important; stroke-width: 2.2px !important; }

    .stButton > button {
        background-color: #FFD500; color: #000; border: 2px solid #000; border-radius: 30px;
        font-weight: 900; text-transform: uppercase; padding: 0.5rem 1.5rem;
        font-size: 0.95rem; width: 100%; margin-top: 0.8rem; height: 48px;
    }

    .stButton > button:hover { background-color: #FF9900; color: #FFF; }

    .card-title { font-size: 1rem; font-weight: 900; color: #111; margin: 0.5rem 0; }

    .ai-grid {
        display: grid !important; grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 10px !important; width: 100% !important; margin: 0 !important;
        padding: 0 !important; box-sizing: border-box !important;
    }

    .ai-card {
        display: flex !important; flex-direction: column !important;
        align-items: center !important; justify-content: center !important;
        background-color: rgba(255,255,255,0.97) !important;
        border: 2px solid #E0E0E0 !important; border-radius: 14px !important;
        padding: 14px 8px !important; text-decoration: none !important;
        color: #000 !important; transition: all 0.2s ease;
        min-height: 105px !important; width: 100% !important;
        box-sizing: border-box !important; margin: 0 !important;
    }

    .ai-card:hover { border-color: #FFD500 !important; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.09); }

    .ai-icon-slot { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-bottom: 9px; }

    .ai-logo { width: 40px !important; height: 40px !important; object-fit: contain !important; display: block !important; margin: 0 !important; }

    .ai-fallback { width: 40px; height: 40px; border-radius: 50%; align-items: center; justify-content: center; font-weight: 900; font-size: 1.1rem; margin: 0; }

    .ai-name { font-weight: 800; font-size: 0.75rem; text-align: center; margin: 0 !important; color: #222; }

    .stCodeBlock pre {
        background: rgba(20,20,20,0.95) !important; color: #FFD500 !important;
        border-radius: 12px; border: 2px solid rgba(255,213,0,0.5);
        font-size: 0.8rem; padding: 10px !important;
    }

    hr { border-color: rgba(0,0,0,0.1); margin: 0.8rem 0; }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 4rem !important;
            padding-bottom: 10vh !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 750px !important;
            margin: 0 auto !important;
        }

        .block-container > div:first-child {
            padding: 1.5rem !important;
            border-radius: 18px !important;
            margin: 0 auto !important;
            width: 100% !important;
        }

        h1 { font-size: 1.5rem !important; }
        .subtitle { font-size: 0.8rem !important; }

        .stButton > button { height: 44px !important; font-size: 0.85rem !important; }
        [data-testid="stChatInput"] { min-height: 48px !important; }
        .ai-grid { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
    }

    @media (max-width: 480px) {
        .block-container {
            padding-top: 4rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 750px !important;
            margin: 0 auto !important;
        }

        .block-container > div:first-child {
            padding: 1.2rem !important;
            border-radius: 16px !important;
            margin: 0 auto !important;
            width: 100% !important;
        }

        h1 { font-size: 1.3rem !important; }

        [data-testid="stAudioInput"] button {
            width: 44px !important;
            height: 44px !important;
        }

        .ai-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 8px !important; }
        .ai-card { min-height: 90px !important; padding: 10px 6px !important; }
        .ai-logo, .ai-fallback { width: 32px !important; height: 32px !important; }
        .ai-name { font-size: 0.65rem !important; }
    }
</style>
""", unsafe_allow_html=True)


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


def optimize_prompt(user_input, domain, tone, depth):
    system = META_SYSTEM + "\n\nDomain: " + DOMAINS.get(domain, DOMAINS["General"])
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": "Domain: " + domain + "\nTone: " + tone + "\nDepth: " + depth + "\n\nRequest:\n" + user_input}
        ],
        temperature=0.4, max_tokens=1500
    )
    return response.choices[0].message.content


def translate_to_english(text):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Translate to English. Output only the translation."},
            {"role": "user", "content": text}
        ],
        temperature=0.1, max_tokens=800
    )
    return response.choices[0].message.content.strip()


def extract_file_text(uploaded_file):
    filename = uploaded_file.name.lower()
    data = uploaded_file.getvalue()
    if filename.endswith(".pdf"):
        import fitz
        document = fitz.open(stream=data, filetype="pdf")
        extracted_text = "\n".join(page.get_text() for page in document)
        document.close()
        return extracted_text
    return data.decode("utf-8", errors="replace")


with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Settings</h2>", unsafe_allow_html=True)
    domain = st.selectbox("Domain", list(DOMAINS.keys()))
    tone = st.selectbox("Tone", ["Professional", "Neutral", "Persuasive", "Instructional"])
    depth = st.selectbox("Depth", ["Concise", "Standard", "Detailed", "Exhaustive"], index=1)
    lang_name = st.selectbox("Audio Language", list(GROQ_LANGS.keys()), index=0)
    st.caption("For Leb Lango, please type instead. Whisper does not support it directly.")


st.markdown('<div class="plg-tag">PROMPTLINE GURU</div>', unsafe_allow_html=True)
st.markdown('<h1>Prompt Better.<br>Build <span class="highlight">Faster.</span></h1>', unsafe_allow_html=True)


st.markdown("""
<style>
@keyframes typewriter {
    from { max-width: 0; }
    to   { max-width: 100%; }
}
.tw-wrap {
    background: rgba(255,255,255,0.95);
    border: 2px solid #FFD500;
    border-radius: 8px;
    padding: 4px 10px;
    margin-bottom: 0.8rem;
    display: inline-block;
    max-width: 100%;
    box-sizing: border-box;
}
.tw-text {
    color: #000;
    font-weight: 800;
    font-size: 0.75rem;
    font-family: monospace;
    text-transform: uppercase;
    margin: 0;
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid #FF9900;
    animation: typewriter 6s steps(60, end) infinite alternate;
}
@media (max-width: 768px) {
    .tw-text { font-size: 0.68rem; }
}
@media (max-width: 480px) {
    .tw-text {
        font-size: 0.62rem;
        white-space: normal;
        word-break: break-word;
        overflow-wrap: anywhere;
        animation: none;
        border-right: none;
    }
}
</style>
<div class="tw-wrap">
    <span class="tw-text">Industry-Grade Production Prompt Engineering</span>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="subtitle">Type, upload, or speak. Instantly generate professional-grade AI prompts.</div>', unsafe_allow_html=True)


col1, col2 = st.columns([10, 1])

with col1:
    chat_val = st.chat_input("Type your request here...", accept_file=True, file_type=["txt", "md", "csv", "pdf"])
    if chat_val:
        if chat_val.text:
            st.session_state["saved_prompt"] = chat_val.text
        if chat_val.files:
            for uploaded_file in chat_val.files:
                st.session_state["saved_prompt"] = extract_file_text(uploaded_file)

with col2:
    audio_val = st.audio_input("", label_visibility="collapsed")
    if audio_val is not None:
        with st.spinner("Transcribing..."):
            try:
                voice_text = client.audio.transcriptions.create(
                    file=("req.wav", audio_val.getvalue()),
                    model="whisper-large-v3",
                    language=GROQ_LANGS[lang_name],
                    response_format="text"
                )
                st.session_state["saved_prompt"] = translate_to_english(voice_text)
                st.toast("Voice captured!")
            except Exception:
                st.error("Mic transcription failed. Please try again or type your request.")


st.markdown("<br>", unsafe_allow_html=True)


if st.button("GENERATE PROMPT", key="gen"):
    final_input = st.session_state.get("saved_prompt", "").strip()
    if not final_input:
        st.warning("Please provide a request (type, upload, or speak).")
        st.stop()

    try:
        with st.spinner("Forging your prompt..."):
            prompt = optimize_prompt(final_input, domain, tone, depth)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">Your Professional Prompt</div>', unsafe_allow_html=True)
        st.code(prompt, language="markdown")
        st.caption("Use the copy icon at the top right of the black box.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">Open prompt with</div>', unsafe_allow_html=True)

        cards = []
        for i, tool in enumerate(AI_TOOLS):
            tool_name = html.escape(tool["name"])
            tool_url = html.escape(tool["url"], quote=True)
            tool_icon = html.escape(tool["icon"], quote=True)
            tool_color = html.escape(tool["color"], quote=True)
            tool_initial = html.escape(tool["initial"])
            fallback_id = f"ai-fallback-{i}"

            card = (
                f'<a href="{tool_url}" target="_blank" rel="noopener noreferrer" class="ai-card">'
                f'<div class="ai-icon-slot">'
                f'<img src="{tool_icon}" alt="{tool_name} logo" class="ai-logo" '
                f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\';" />'
                f'<div id="{fallback_id}" class="ai-fallback" style="display:none;background-color:{tool_color};color:#ffffff;">{tool_initial}</div>'
                f'</div>'
                f'<p class="ai-name">{tool_name}</p>'
                f'</a>'
            )
            cards.append(card)

        grid_html = '<div class="ai-grid">' + "".join(cards) + '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

    except Exception as error:
        st.error("Something went wrong while generating your prompt. Please check your Groq API configuration and try again.")
        st.exception(error)
