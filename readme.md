# 🛍️ AI Customer Support Bot

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.2-orange?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4-blueviolet?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama3.1-brightgreen?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?style=flat-square&logo=streamlit)
![Deploy](https://img.shields.io/badge/Deployed-Streamlit_Cloud-ff4b4b?style=flat-square)

A **RAG-based AI customer support chatbot** that answers customer queries exclusively from a custom knowledge base — no hallucination, no out-of-scope answers. Built using Retrieval-Augmented Generation (RAG) with LangChain, ChromaDB and Groq.

🌐 **Live Demo:** [customer-support-bot-zxn8vshhqgr28d77soz4ux.streamlit.app](https://customer-support-bot-zxn8vshhqgr28d77soz4ux.streamlit.app/)

---

## 🔍 How It Works

```
User asks a question
          │
          ▼
LangChain receives the query
          │
          ▼
ChromaDB searches FAQ knowledge base    ← finds top 3 most relevant chunks
          │
          ▼
Relevant chunks passed to Groq as context
          │
          ▼
Groq generates answer ONLY from context ← no hallucination
          │
          ▼
Answer displayed in chat UI
```

---

## ✨ Features

- **RAG architecture** — answers grounded in your knowledge base only
- **Hallucination prevention** — system prompt restricts LLM to provided context
- **Pre-ingested knowledge base** — FAQ data loaded into ChromaDB at startup
- **Persistent vector store** — ChromaDB saved to disk, no reprocessing on restart
- **Chat interface** — full conversation history with session state
- **Graceful fallback** — redirects to support email when answer not found

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Document Loading | LangChain TextLoader |
| Text Splitting | RecursiveCharacterTextSplitter |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector Store | ChromaDB (persistent) |
| LLM | Groq (Llama 3.1 8B) via LangChain |
| Orchestration | LangChain LCEL |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/sachmundassery/customer-support-bot.git
cd customer-support-bot

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# Install dependencies
pip install -r requirements.txt
```

Create `.env` file:
```env
GROQ_API_KEY=your_groq_key_here
```

Ingest FAQ data into ChromaDB:
```bash
python ingest.py
```

Run the app:
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
customer-support-bot/
│
├── data/
│   └── faq.txt          ← Knowledge base (FAQ data)
├── tests/
│   ├── test_gemini.py   ← LLM connectivity test
│   ├── test_langchain.py← LangChain chain test
│   ├── test_chromaDb.py ← ChromaDB vector search test
│   └── test_streamlit.py← Streamlit UI test
├── chroma_db/           ← Persisted vector store (auto-generated)
├── ingest.py            ← Loads FAQ into ChromaDB
├── app.py               ← Streamlit chatbot UI
├── requirements.txt
├── .env
└── .gitignore
```

---

## 💡 Key Design Decisions

**Why RAG over fine-tuning?**  
Fine-tuning requires expensive compute and retraining when data changes. RAG retrieves relevant context at query time — cheaper, faster to update and more reliable for factual accuracy.

**Why persistent ChromaDB?**  
FAQ data is static and known upfront. Persisting to disk means the vector store loads instantly on startup — no reprocessing required on each deployment.

**Why restrict LLM to context only?**  
Unrestricted LLMs hallucinate answers confidently. By restricting the system prompt to provided context only, the bot stays trustworthy and on-topic — critical for customer-facing applications.

---

## 🧑‍💻 Author

**Sachin Mundassery**  
[![GitHub](https://img.shields.io/badge/GitHub-sachmundassery-black?style=flat-square&logo=github)](https://github.com/sachmundassery)

---

## 📄 License

MIT License