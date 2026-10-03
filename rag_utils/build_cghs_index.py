
import os
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import joblib

PROJECT_DIR = "/content/drive/MyDrive/cghs-ai-prototype"
DOCS_DIR = Path(PROJECT_DIR) / "data" / "cghs_docs"

docs = []
for pdf_path in DOCS_DIR.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf_path))
    docs.extend(loader.load())

print(f"Loaded {len(docs)} document chunks from PDFs.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    length_function=len
)
splits = text_splitter.split_documents(docs)
print(f"Created {len(splits)} text splits.")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(splits, embeddings)

INDEX_PATH = Path(PROJECT_DIR) / "rag_utils" / "cghs_faiss_index"
vectorstore.save_local(str(INDEX_PATH))
print("FAISS index saved to:", INDEX_PATH)

meta = {
    "docs_dir": str(DOCS_DIR),
    "num_splits": len(splits)
}
joblib.dump(meta, str(INDEX_PATH) + "_meta.pkl")
