from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return db


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
