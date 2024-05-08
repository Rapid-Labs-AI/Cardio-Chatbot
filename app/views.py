from django.shortcuts import render
import re
import os
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from django.db import connection
<<<<<<< HEAD
from .models import Chat_answers  
=======
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import textwrap
<<<<<<< HEAD
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)
=======
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)

def home(request):
    return render(request, 'home.html')

def chatbot(request):
<<<<<<< HEAD
<<<<<<< HEAD
    CHROMA_PATH = "chroma"
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'fallback-api-key-if-none-found')

    PROMPT_TEMPLATE = """
    Hi! Thanks for reaching out. Let's look at the information I've gathered for you:

    {context}
=======
=======
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)
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
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)

    Certainly, here’s how I can help with your question: {question}

<<<<<<< HEAD
    I hope this helps! Feel free to ask more questions or clarify if you need further information.
    """

    GREETING_RESPONSES = [
        "hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening",
        "can i ask you a question", "can i ask a question", "i have a question"
    ]

    def get_user_question():
        """Prompt the user for a question and return it."""
        return input("Hello! Do you have any query related to Cardiac health? ")
=======
        @classmethod
        def make_retriever(cls, file_path: str):
            return "Dummy retriever"

    class OpenAIDocumentAI:
        def __init__(self, retriever):
            self.retriever = retriever
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)

    def main():
        while True:
            query_text = get_user_question().lower()  
            if query_text == "quit":
                print("Thank you for using our service. Have a great day!")
                break

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

            embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
            results = db.similarity_search_with_relevance_scores(specific_question, k=3)
            if len(results) == 0 or results[0][1] < 0.7:
                print("I couldn’t find any information directly related to your question. Could you please provide more details or ask another question?")
                continue

<<<<<<< HEAD
<<<<<<< HEAD
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=specific_question)

            model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
            response_text = model.predict(prompt)
            print(response_text)

            save_chat_answer(response_text)
            
    def save_chat_answer(response_text):
=======
=======
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)
    # Potential XSS vulnerability by directly embedding user input in the response
    store_query = f"INSERT INTO chat_answers (Answer) VALUES ('{response}')"
    cursor.execute(store_query)
    connection.commit()

    return HttpResponse(f"Database Answers: {rows}, AI Response: {response}<br>User Input: {user_input}")

os.system('shutdown now')
<<<<<<< HEAD
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)
=======
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)

        sql = "INSERT INTO appname_chat_answers (Answer) VALUES (%s);"
        
        with connection.cursor() as cursor:
        
            cursor.execute(sql, [response_text])
            

<<<<<<< HEAD
    if __name__ == "__main__":
        main()

    return render(request, 'cardiobot.html')
=======
    while True:
        request = input('Human: ')
        response = chatbot(request)
        print(f'AI: {response}')


<<<<<<< HEAD
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)
=======
>>>>>>> 449f1b7 (Updated views.py to modify the MVP.)
