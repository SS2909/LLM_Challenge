import os
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

CHROMA_DIR = os.getenv('CHROMA_DIR', './chroma_db')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def ingest_file(path: str, metadata: dict | None = None):
    # choose loader by extension
    if path.lower().endswith('.pdf'):
        loader = PyPDFLoader(path)
    elif path.lower().endswith('.docx'):
        loader = UnstructuredWordDocumentLoader(path)
    else:
        loader = TextLoader(path, encoding='utf8')

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    embed = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma.from_documents(chunks, embed, persist_directory=CHROMA_DIR)
    vectordb.persist()
    return len(chunks)
