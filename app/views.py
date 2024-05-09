from django.shortcuts import render
import re
import os
<<<<<<< HEAD
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from django.db import connection
from .models import Chat_answers  
=======
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
>>>>>>> 2dd1eea (Modified to add random number generation)

def home(request):
    return render(request, 'home.html')

def chatbot(request):
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

<<<<<<< HEAD
    def main():
        while True:
            query_text = get_user_question().lower()  
            if query_text == "quit":
                print("Thank you for using our service. Have a great day!")
                break
=======
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
>>>>>>> 2dd1eea (Modified to add random number generation)

            parts = re.split(r'[?.!]\s*', query_text)
            greeting_part = None
            specific_question = None
            for part in parts:
                if any(greeting in part for greeting in GREETING_RESPONSES):
                    greeting_part = part
                else:
                    if part.strip():
                        specific_question = part

            if greeting_part and not specific_question:
                print("Hello! I'm here to help you with any questions you might have about mental health. What would you like to know more about?")
                continue

<<<<<<< HEAD
            embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
            results = db.similarity_search_with_relevance_scores(specific_question, k=3)
            if len(results) == 0 or results[0][1] < 0.7:
                print("I couldn’t find any information directly related to your question. Could you please provide more details or ask another question?")
                continue
=======
    return HttpResponse(f"Database Answers: {rows}, AI Response: {response}<br>User Input: {user_input}<br>Random Numbers: {random_numbers}")
>>>>>>> 2dd1eea (Modified to add random number generation)

            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=specific_question)

            model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
            response_text = model.predict(prompt)
            print(response_text)

<<<<<<< HEAD
            save_chat_answer(response_text)
            
    def save_chat_answer(response_text):

        sql = "INSERT INTO appname_chat_answers (Answer) VALUES (%s);"
        
        with connection.cursor() as cursor:
        
            cursor.execute(sql, [response_text])
            

    if __name__ == "__main__":
        main()

    return render(request, 'cardiobot.html')
=======
    while True:
        request = input('Human: ')
        response = chatbot(request)
        print(f'AI: {response}')
>>>>>>> 2dd1eea (Modified to add random number generation)
