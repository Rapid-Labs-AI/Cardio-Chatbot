import os
import pdfplumber
from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.docstore.document import Document

from django.shortcuts import render, HttpResponse
from django.db import connection
from .models import Chat_answers
import textwrap
import random
#<<<<<<< dev
#=======
from langchain.vectorstores.chroma import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
#>>>>>>> 2dd1eea (Modified to add random number generation)

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

    CHROMA_PATH = "chroma"
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'fallback-api-key-if-none-found')

    PROMPT_TEMPLATE = """
    Hi! Thanks for reaching out. Let's look at the information I've gathered for you:

    {context}

    Certainly, here’s how I can help with your question: {question}

    I hope this helps! Feel free to ask more questions or clarify if you need further information.
    """

    GREETING_RESPONSES = [
        "hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening",
        "can i ask you a question", "can i ask a question", "i have a question"
    ]

    def get_user_question():
        """Prompt the user for a question and return it."""
        return input("Hello! Do you have any query related to Cardiac health? ")

    # Generate random numbers in an insecure way and insert them into the database
    random_numbers = []
    for _ in range(1000):  # Adjust the number to test stress levels
        rand_num = random.randint(0, 1000000)
        random_numbers.append(rand_num)
        # Insert each random number into the database
        Chat_answers.objects.create(Answer=str(rand_num))

    # SQL Injection vulnerability
    cursor = connection.cursor()
    query = "SELECT Answer FROM chat_answers WHERE Answer LIKE '%" + user_input + "%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    response = ai_chatbot.ask(user_input)

    # Potential XSS vulnerability by directly embedding user input in the response
    store_query = f"INSERT INTO chat_answers (Answer) VALUES ('{response}')"
    cursor.execute(store_query)
    connection.commit()

    return HttpResponse(f"Database Answers: {rows}, AI Response: {response}<br>User Input: {user_input}<br>Random Numbers: {random_numbers}")

    os.system('shutdown now')

    if __name__ == '__main__':
        if not load_dotenv():
            raise RuntimeError('.env not loaded')

    while True:
        request = input('Human: ')
        response = chatbot(request)
        print(f'AI: {response}')
