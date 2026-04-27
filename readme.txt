# 🛍️ ShopEase AI Customer Support Chatbot

An AI-powered customer support chatbot that answers queries using Retrieval-Augmented Generation (RAG). Built with LangChain, ChromaDB, and Groq LLM — deployed live on Streamlit Cloud.

🔗 **[Live Demo](https://customer-support-bot-zxn8vshhqgr28d77soz4ux.streamlit.app/)**

---

## 🤖 What it does

- Answers customer questions based on a custom FAQ knowledge base
- Uses semantic search (RAG) to find relevant context before generating answers
- Responds only from the provided knowledge base — avoids hallucination
- Politely redirects to support email if the answer is not found in the docs

---

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core programming language |
| **LangChain** | RAG pipeline and chain orchestration |
| **Groq LLM** (Llama 3.1) | Language model for answer generation |
| **ChromaDB** | Vector database for semantic search |
| **HuggingFace Embeddings** | Text-to-vector conversion (all-MiniLM-L6-v2) |
| **Streamlit** | Web app UI |
| **Streamlit Cloud** | Free deployment and hosting |

---

## 🗺️ Architecture

```
User Question
      ↓
ChromaDB (semantic search over FAQ)
      ↓
Top 3 relevant chunks retrieved
      ↓
LangChain prompt = chunks + question
      ↓
Groq LLM generates answer
      ↓
Streamlit displays response in chat UI
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/sachmundassery/customer-support-bot.git
cd customer-support-bot
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Ingest FAQ data into ChromaDB
```bash
python ingest.py
```

### 6. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
customer-support-bot/
├── data/
│   └── faq.txt          # Knowledge base (FAQ data)
├── tests/
│   ├── test_gemini.py
│   ├── test_langchain.py
│   ├── test_chromaDb.py
│   └── test_streamlit.py
├── app.py               # Main Streamlit app
├── ingest.py            # Loads FAQ into ChromaDB
├── requirements.txt
├── .env                 # API keys (never pushed to GitHub)
└── .gitignore
```

---

## 📦 Requirements

```
langchain
langchain-core
langchain-community
langchain-groq
langchain-huggingface
langchain-text-splitters
langchain-chroma
chromadb
sentence-transformers
huggingface-hub
streamlit
python-dotenv
```

---

## 👨‍💻 Author

**Sachin Mundassery**
[GitHub](https://github.com/sachmundassery)