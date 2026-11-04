import streamlit as st
import html

# AI tool cards
ai_cards_html = """
<style>
.ai-tools-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 15px;
}

.ai-tool-card {
    width: 115px;
    min-height: 105px;
    padding: 14px 8px;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    background: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    text-decoration: none !important;
    transition: all 0.2s ease;
}

.ai-tool-card:hover {
    transform: translateY(-4px);
    border-color: #f5b82e;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

.ai-tool-card img {
    width: 40px;
    height: 40px;
    object-fit: contain;
    display: block;
    margin-bottom: 10px;
}

.ai-tool-name {
    color: #222;
    font-size: 13px;
    font-weight: 600;
}

.ai-fallback {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: none;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
<div class="ai-tools-container">
"""

for tool in AI_TOOLS:
    name = html.escape(tool["name"])
    url = html.escape(tool["url"], quote=True)
    icon = html.escape(tool["icon"], quote=True)
    color = html.escape(tool.get("color", "#444"), quote=True)
    initial = html.escape(name[0].upper())

    ai_cards_html += f"""
    <a class="ai-tool-card" href="{url}" target="_blank" rel="noopener noreferrer">
        <img
            src="{icon}"
            alt="{name}"
            onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
        >
        <div class="ai-fallback" style="background:{color}20; color:{color};">
            {initial}
        </div>
        <div class="ai-tool-name">{name}</div>
    </a>
    """

ai_cards_html += "</div>"

# IMPORTANT: This must be True
st.markdown(ai_cards_html, unsafe_allow_html=True)
