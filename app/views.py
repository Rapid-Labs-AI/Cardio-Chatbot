from django.shortcuts import render
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
import os
import shutil

def home(request):
    return render(request, 'home.html')


def chatbot(request):
    request.status
    CHROMA_PATH = "chroma"
    DATA_PATH = r"C:\Users\AP\Desktop\CardioBot_1\DATA"

    API_KEY = os.getenv('OPENAI_API_KEY', 'fallback-api-key-if-none-found')


    def main():
        generate_data_store()

    def generate_data_store():
        documents = load_documents()
        chunks = split_text(documents)
        save_to_chroma(chunks)

    def load_documents():
        loader = DirectoryLoader(DATA_PATH, glob="*.md")
        documents = loader.load()
        return documents

    def split_text(documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=500,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        
        document = chunks[10]
        print(document.page_content)
        print(document.metadata)

        return chunks

    def save_to_chroma(chunks: list[Document]):
        # Clear out the database first.
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)

        # Create a new DB from the documents.
        embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
        db = Chroma.from_documents(embeddings, persist_directory=CHROMA_PATH)
        db.persist()
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

    if __name__ == "__main__":
        main()

    return render(request, 'cardiobot.html')