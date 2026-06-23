# 🩺 VitalAI

> AI-powered health analysis agent — upload your blood reports and get instant insights, RAG-powered follow-up Q&A, and multi-model LLM cascade.

Built with **LangChain · FAISS · Groq · Supabase · Python**

---

## ✨ Features

- 🧠 **Analysis Agent** — deep blood report analysis with in-context learning from a built-in medical knowledge base
- 💬 **Chat Agent** — RAG-powered follow-up Q&A over your report using FAISS + HuggingFace embeddings
- 🔄 **Multi-model LLM Cascade** — automatic fallback across Groq models (Llama 4 → Llama 3.3 → Llama 3.1)
- 📄 **PDF Upload** — upload your own blood report (up to 20MB, 50 pages) or use the built-in sample
- 🔐 **Secure Auth** — Supabase Auth with session validation and configurable timeout
- 🗂️ **Session History** — create, switch, and delete analysis sessions; all data persisted across reloads
- 📊 **Daily Limit** — configurable analysis cap (default 15/day) with live countdown in sidebar

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq (Llama 4 Maverick, Llama 3.3 70B, Llama 3.1 8B) |
| RAG | LangChain + FAISS + HuggingFace (all-MiniLM-L6-v2) |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth + Gotrue |
| PDF | PDFPlumber + filetype |

---

## 🤖 LLM Architecture

```
User uploads PDF
       ↓
PDF Extractor → validates file type + medical content
       ↓
Analysis Agent → Groq multi-model cascade
       ├── Primary:   meta-llama/llama-4-maverick-17b-128e-instruct
       ├── Secondary: llama-3.3-70b-versatile
       ├── Tertiary:  llama-3.1-8b-instant
       └── Fallback:  llama3-70b-8192
       ↓
RAG Chat Agent → FAISS vector store + HuggingFace embeddings
       ↓
Follow-up Q&A over your report
```

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- Supabase account
- Groq API key

### Installation

```bash
git clone https://github.com/Haneesh-Nellore/VitalAI.git
cd VitalAI/hia-main
pip install -r requirements.txt
```

### Environment Setup

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
GROQ_API_KEY = "your-groq-api-key"
```

### Database Setup

Run the SQL script to create required tables:

```bash
psql -f public/db/script.sql
```

Or paste it directly in your Supabase SQL editor.

### Run

```bash
streamlit run src/main.py
```

---

## 📁 Project Structure

```
VitalAI/
└── hia-main/
    ├── src/
    │   ├── main.py                 # App entry point
    │   ├── agents/
    │   │   ├── analysis_agent.py   # Report analysis + knowledge base
    │   │   ├── chat_agent.py       # RAG pipeline (FAISS + embeddings)
    │   │   └── model_manager.py    # Groq multi-model cascade
    │   ├── services/
    │   │   └── ai_service.py       # Analysis + chat entry points
    │   ├── auth/
    │   │   ├── auth_service.py     # Supabase auth + persistence
    │   │   └── session_manager.py  # Session lifecycle management
    │   ├── components/
    │   │   ├── analysis_form.py    # Report upload + analysis trigger
    │   │   ├── sidebar.py          # Session list + daily limit
    │   │   └── auth_pages.py       # Login / signup UI
    │   ├── config/
    │   │   ├── app_config.py       # App limits and settings
    │   │   └── prompts.py          # Specialist LLM prompts
    │   └── utils/
    │       ├── validators.py       # Email, password, PDF validation
    │       └── pdf_extractor.py    # PDF text extraction
    └── public/
        └── db/
            ├── script.sql          # Supabase schema
            └── schema.png          # DB diagram
```

---

## 🔮 Roadmap

- [ ] AWS Lambda deployment for serverless scaling
- [ ] API Gateway integration for mobile client support
- [ ] Redis caching layer for repeated report analysis
- [ ] Multi-report comparison across sessions
- [ ] Terraform IaC for full cloud deployment

---

## 📄 License

MIT License — based on the open-source HIA project, extended and maintained by [Haneesh Nellore](https://github.com/Haneesh-Nellore).
