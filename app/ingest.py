from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
import fickling

api_key = os.environ.get["OPENAI_API_KEY"]
DATA_PATH = 'data/'
DB_FAISS_PATH = 'vectorstore/db_faiss'
# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
                                                   chunk_size=510,
                                                   chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', api_key=api_key)
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    data = fickling.load('data/index.pkl')
    return data
if __name__ == "__main__":
    data = create_vector_db()
