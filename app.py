from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

'''
Loads the chroma_db/ folder we created with ingest.py
@st.cache_resource means — load this once and reuse it. Don't reload every time the user sends a message. Makes it fast.
'''
@st.cache_resource
def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return db

'''
This is the heart of the bot. Let me explain each piece:

retriever — searches ChromaDB and fetches top 3 most relevant FAQ chunks for any question
prompt — the instructions we give to Groq. We tell it to ONLY answer from the context — this stops it from making things up
RunnablePassthrough() — just passes the user's question through as-is
chain = retriever | prompt | llm | StrOutputParser() — this is the pipeline:

User question
     ↓
retriever finds relevant FAQ chunks
     ↓
prompt combines chunks + question into one message
     ↓
llm (Groq) generates the answer
     ↓
StrOutputParser converts it to plain text string

'''

@st.cache_resource
def load_chain():
    db = load_db()
    llm = ChatGroq(model="llama-3.1-8b-instant")
    retriever = db.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful customer support agent for ShopEase store.
    Answer the customer's question using ONLY the context below.
    If the answer is not in the context, say "I'm sorry, I don't have information on that. Please contact us at support@shopease.com"

    Context: {context}

    Question: {question}

    Answer:""")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

# --- Streamlit UI ---

'''
st.title and st.caption — the heading and subtitle you see on screen
st.session_state.messages — this is how Streamlit remembers chat history. Every time the page refreshes, this keeps the conversation intact
The for loop — rerenders all previous messages so the chat history stays visible
'''
st.title("🛍️ ShopEase Customer Support")
st.caption("Ask me anything about orders, shipping, returns and more!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

chain = load_chain()

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = chain.invoke(prompt)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})




# User types: "How long does shipping take?"
#                    ↓
#          ChromaDB searches faq.txt
#          finds: "Shipping takes 3-5 days"
#                    ↓
#          Prompt = "You are support agent...
#                    Context: Shipping takes 3-5 days
#                    Question: How long does shipping take?"
#                    ↓
#          Groq generates: "Standard shipping takes
#                           3-5 business days!"
#                    ↓
#          Streamlit displays it in chat UI 
