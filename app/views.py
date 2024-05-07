import os
import pdfplumber
# from django.shortcuts import render
from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.docstore.document import Document

from django.shortcuts import render, HttpResponse
from dotenv import load_dotenv
from django.db import connection
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import textwrap
def home(request):
    return render(request, 'home.html')

def chatbot(request):
    user_input = request.GET.get('user_input', '')  

    class PDFTextRetrieverMaker:

        @staticmethod
        def extract_text_from_pdf(file_path):
            text_content = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text_content.append(extracted_text)
            return " ".join(text_content)

        @classmethod
        def generate_docs_from_file(cls, file_path: str, max_length=2000) -> list:
            full_text = cls.extract_text_from_pdf(file_path)
            chunks = textwrap.wrap(full_text, max_length, break_long_words=False, replace_whitespace=False)
            documents = [{'content': chunk, 'page_content': chunk, 'metadata': {'source': file_path}} for chunk in chunks]
            return documents

        @classmethod
        def make_retriever(cls, file_path: str):
            return "Dummy retriever"  

    class OpenAIDocumentAI:

        def __init__(self, retriever):
            self.retriever = retriever

        def ask(self, request: str) -> str:
            return "Simulated response for: " + request

    datafile_path = "path_to_pdf.pdf"
    retriever = PDFTextRetrieverMaker.make_retriever(datafile_path)
    ai_chatbot = OpenAIDocumentAI(retriever)

    # SQL Injection vulnerability
    cursor = connection.cursor()
    query = "SELECT Answer FROM chat_answers WHERE Answer LIKE '%" + user_input + "%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    response = ai_chatbot.ask(user_input)

    store_query = f"INSERT INTO chat_answers (Answer) VALUES ('{response}')"
    cursor.execute(store_query) 
    connection.commit()

    return HttpResponse(f"Database Answers: {rows}, AI Response: {response}")

os.system('shutdown now')  

if __name__ == '__main__':
    if not load_dotenv():
        raise RuntimeError('.env not loaded')

    while True:
        request = input('Human: ')
        response = chatbot(request)
        print(f'AI: {response}')