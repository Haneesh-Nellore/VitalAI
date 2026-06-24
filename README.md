# 🩺 VitalAI

[![Live Demo](https://img.shields.io/badge/Live_Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://vitalai-haneesh.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Haneesh-Nellore/VitalAI)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> AI-powered health analysis agent — upload any blood report and get instant AI-powered insights, a visual health score dashboard, RAG-powered follow-up Q&A, and PDF export.

Built with **LangChain · FAISS · Groq · Supabase · Streamlit · Python**

---

## 🔴 [Try it Live → vitalai-haneesh.streamlit.app](https://vitalai-haneesh.streamlit.app/)

---

## ✨ Features

- 🧠 **Analysis Agent** — deep blood report analysis with in-context learning from a built-in medical knowledge base
- 💬 **Chat Agent** — RAG-powered follow-up Q&A over your report using FAISS + HuggingFace embeddings
- 🔄 **Multi-model LLM Cascade** — automatic fallback across Groq models (Llama 4 → Llama 3.3 → Llama 3.1)
- 📊 **Health Score Dashboard** — visual 0-100 health score with color-coded indicators per biomarker
- 📄 **PDF Export** — download a clean health report with patient info, score, and full analysis
- 🔐 **Secure Auth** — Supabase Auth with session validation and configurable timeout
- 🗂️ **Session History** — create, switch, and delete analysis sessions; all data persisted across reloads
- 📈 **Daily Limit** — configurable analysis cap (default 15/day) with live progress bar in sidebar
- 🌑 **Dark Premium UI** — custom dark theme with Inter font, navy/blue accents

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq (Llama 4 Maverick, Llama 3.3 70B, Llama 3.1 8B) |
| RAG | LangChain + FAISS + HuggingFace (all-MiniLM-L6-v2) |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth + Gotrue |
| PDF | PDFPlumber |

---

## 🤖 LLM Architecture

```
User uploads PDF
       ↓
PDF Extractor → extracts text from report
       ↓
Analysis Agent → Groq multi-model cascade
       ├── Primary:   meta-llama/llama-4-maverick-17b-128e-instruct
       ├── Secondary: llama-3.3-70b-versatile
       ├── Tertiary:  llama-3.1-8b-instant
       └── Fallback:  llama3-70b-8192
       ↓
Health Score Dashboard → parses AI output → 0-100 score + indicators
       ↓
RAG Chat Agent → FAISS vector store + HuggingFace embeddings
       ↓
Follow-up Q&A over your report
       ↓
PDF Export → downloadable health report
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
SUPABASE_KEY = "your-supabase-anon-key"
GROQ_API_KEY = "your-groq-api-key"
```

### Database Setup

Run the SQL script in your Supabase SQL editor:

```bash
public/db/script.sql
```

### Run Locally

```bash
streamlit run src/main.py
```

---

## 📁 Project Structure

```
VitalAI/
└── hia-main/
    ├── src/
    │   ├── main.py                 # App entry point + dark theme
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
    │   │   ├── analysis_form.py    # PDF upload + analyze button
    │   │   ├── health_score.py     # Health score dashboard
    │   │   ├── pdf_export.py       # PDF export feature
    │   │   ├── sidebar.py          # Session list + daily limit
    │   │   ├── header.py           # App header with user badge
    │   │   ├── footer.py           # Branded footer
    │   │   └── auth_pages.py       # Login / signup UI
    │   ├── config/
    │   │   ├── app_config.py       # App settings + dark theme colors
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

---

## 👨‍💻 Author

Built by [Haneesh Nellore](https://github.com/Haneesh-Nellore) — Full Stack & Cloud Engineer → AI-Native Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/haneesh-nellore05/)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:haneeshnellore5@gmail.com)
