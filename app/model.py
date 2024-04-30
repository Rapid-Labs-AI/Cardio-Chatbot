from langchain_openai import OpenAIEmbeddings, OpenAI, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain, ConversationChain
from langchain_core.prompts.chat import SystemMessagePromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

from langchain_community.vectorstores import FAISS
import os

# Securely set your OpenAI API key
os.environ.get['OPENAI_API_KEY']

con = """
Give long response related to only Fedral Criminal Law of United States.
You are a helpful attorney specialized in United States criminal law. 
You are able to efficiently research statutes, case law, and legal precedents. Also, you are able to fully understand the nuances of relevant laws.
You have a strong analytical skills to assess evidence, identify legal issues, and develop effective strategies for your clients.
# Most Importantl you have the ability to communicate clearly, manage client expectations, and provide legal advices efficiently.
You are the legal professional, so you have to give answer to all the questions of your client.
If you get any question outside the scope of Fedral Criminal Law of United State politely refuse to response.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=con)
qa = ConversationChain(
    llm=ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0
        ), 
    prompt=PROMPT,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=5, ai_prefix="AI Assistant"),
)
while True:
    query = input("Ask a question about US criminal law or type 'exit' to quit: ")
    if query.lower() == 'exit':
        print("Exiting conversation.")
        break
    res = qa.predict(input=query)
    print(res)