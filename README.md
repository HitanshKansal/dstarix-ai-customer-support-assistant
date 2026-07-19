# DStarix Techno AI Customer Support Assistant

## Project Title

DStarix Techno AI Customer Support Assistant

## Project Description

This project is a Streamlit-based AI customer support chatbot for DStarix Techno. It uses Python, LangChain, and Groq to answer customer questions in a professional and context-aware way.

Live app: https://dstarix-ai-customer-support-assistant.onrender.com

The assistant uses a static verified knowledge base from `knowledge.py`. It does not scrape LinkedIn, does not browse live job posts at runtime, and does not invent current openings.

## Features

- ChatGPT-style Streamlit chat interface.
- DStarix Techno branded UI with logo.
- Saved previous chats in the sidebar.
- New chat and delete previous chat controls.
- LangChain prompt, model, parser, and chain structure.
- Groq LLM integration using `langchain-groq`.
- Static company knowledge base for DStarix Techno services, careers, FAQs, and contact links.
- Safe response behavior when information is missing from the knowledge base.
- Environment variable support with `python-dotenv`.
- Basic protection when the Groq API key is missing.

## Technologies Used

- Python
- Streamlit
- LangChain
- LangChain Core
- LangChain Groq
- Groq API
- python-dotenv

## Installation Instructions

Clone the repository:

```powershell
git clone https://github.com/HitanshKansal/dstarix-ai-customer-support-assistant.git
cd dstarix-ai-customer-support-assistant
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Setup Instructions

Create a `.env` file in the project root:

```text
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b
```

Add your real Groq API key after `GROQ_API_KEY=`.

Do not commit `.env`. The `.gitignore` file is configured to keep `.env`, `venv/`, Python cache files, and local chat history out of Git.

If Groq changes model availability, update `GROQ_MODEL` to a supported Groq chat model.

## Usage Guide

Run the Streamlit app:

```powershell
streamlit run app.py
```

Or run Streamlit from the virtual environment:

```powershell
.\venv\Scripts\streamlit.exe run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Render Deployment

This repository includes `render.yaml` for Render Blueprint deployment.

Live Render deployment:

```text
https://dstarix-ai-customer-support-assistant.onrender.com
```

On Render:

1. Create a new Blueprint or Web Service from this GitHub repository.
2. Use the `main` branch.
3. When Render asks for environment variables, add your real Groq API key for `GROQ_API_KEY`.
4. Keep `GROQ_MODEL` as `openai/gpt-oss-20b` unless you want to use another supported Groq chat model.

Render uses this start command from `render.yaml`:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

Example questions:

- What services does DStarix Techno provide?
- Tell me about Agentic AI solutions.
- How can I start a project?
- Are you currently hiring?
- Where can I see current job openings?
- How does DStarix ensure data security?

For careers questions, the assistant should direct users to official sources:

- DStarix Careers: https://www.dstarix.in/careers
- DStarix LinkedIn Jobs: https://www.linkedin.com/company/dstarix-techno/jobs/

## Project Structure

```text
.
|-- app.py
|-- knowledge.py
|-- prompts.py
|-- requirements.txt
|-- render.yaml
|-- README.md
|-- .env.example
|-- .gitignore
|-- .streamlit/
|   `-- config.toml
`-- assets/
    |-- logo.jpeg
    `-- logo-cropped.png
```

## Notes

- `.env` is required locally but must not be committed.
- `chat_sessions.json` stores local chat history and is ignored by Git.
- The assistant does not browse websites or scrape LinkedIn dynamically.
- Current openings should be updated manually in `knowledge.py` only after checking official sources.
