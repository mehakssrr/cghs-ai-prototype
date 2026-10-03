
from pathlib import Path
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
import os

PROJECT_DIR = "/content/drive/MyDrive/cghs-ai-prototype"
INDEX_PATH = Path(PROJECT_DIR) / "rag_utils" / "cghs_faiss_index"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    str(INDEX_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)

llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",
    model_kwargs={
        "temperature": 0.1,
        "max_length": 512
    }
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

def answer_cghs_question(question: str) -> dict:
    result = qa_chain({"query": question})
    answer = result["result"]
    sources = []
    for doc in result.get("source_documents", []):
        sources.append({
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", None),
            "text": doc.page_content[:300]
        })
    return {
        "answer": answer,
        "sources": sources
    }
