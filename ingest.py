from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

print("Loading FAQ data...")
loader = TextLoader("data/faq.txt")
documents = loader.load()

print("Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

print("Creating embeddings and storing in ChromaDB...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="chroma_db"
)

print("✅ Done! FAQ data ingested into ChromaDB successfully!")
print(f"Total chunks stored: {len(chunks)}")