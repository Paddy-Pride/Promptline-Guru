# Promptline Guru

Plain language in, professional AI instructions out.

Promptline Guru is a prompt engineering assistant. A user describes what they want in plain language, selects a domain, tone, and depth, and Promptline Guru returns a single production-ready prompt structured to professional standards.

Every generated prompt contains seven sections:

1. ROLE
2. OBJECTIVE
3. CONTEXT AND CONSTRAINTS
4. INPUTS
5. PROCESS
6. OUTPUT FORMAT
7. QUALITY BAR

The QUALITY BAR section forces concrete, checkable success criteria into every prompt. That is what separates professional AI output from generic output.

## Features

- Nine domain profiles: General, Software Engineering, Business, Education, Health, Agriculture, Government, Creative, Research
- Tone control: Professional, Neutral, Persuasive, Instructional, Conversational
- Depth control: Concise, Standard, Detailed, Exhaustive
- Voice input via Groq Whisper (whisper-large-v3-turbo)
- Editable transcript before generation
- Production-safe model selection (openai/gpt-oss-120b on Groq)

## Run locally

    pip install -r requirements.txt
    export GROQ_API_KEY="gsk_your_key_here"
    streamlit run app.py

On Windows PowerShell:

    $env:GROQ_API_KEY="gsk_your_key_here"
    streamlit run app.py

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to share.streamlit.io and create a new app pointing to app.py.
3. In Advanced settings, add a secret: GROQ_API_KEY = "gsk_your_key_here".
4. Deploy.

## Deploy on GitHub Codespaces

1. Open the repo in Codespaces.
2. Add GROQ_API_KEY as a Codespaces secret.
3. In the terminal:
   pip install -r requirements.txt
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
4. Click the forwarded port link.

## Tech

- Streamlit for the interface
- Groq API for prompt generation (openai/gpt-oss-120b)
- Groq Whisper for voice transcription (whisper-large-v3-turbo)

## License

MIT. See LICENSE.
