# LLM Chat App (Streamlit + FastAPI + RAG)

This is a sample project scaffold demonstrating:
- FastAPI backend with simple JWT-like auth (token created via jose)
- Streamlit frontend for login, upload, and chat
- Document ingestion with LangChain + Chroma (local)
- OpenAI-based LLM calls (you must set OPENAI_API_KEY)

## Quick start (dev)

1. Create a virtualenv and activate it.
2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
3. Install requirements: `pip install -r requirements.txt`
4. Run backend: `uvicorn backend.app.main:app --reload --port 8000`
5. Run Streamlit: `streamlit run streamlit_app/app.py`

