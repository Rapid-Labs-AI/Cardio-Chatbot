import os
import pdfplumber
from django.shortcuts import render
from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import textwrap
def home(request):
    return render(request, 'home.html')

def chatbot(request):
    class PDFTextRetrieverMaker:
    
        @staticmethod
        def extract_text_from_pdf(file_path):
            text_content = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:  # Add text only if it is not None
                        text_content.append(extracted_text)
            return " ".join(text_content)

        @classmethod
        def generate_docs_from_file(cls, file_path: str,  max_length=2000) -> list[Document]:
            full_text = cls.extract_text_from_pdf(file_path)
            document_text = cls.extract_text_from_pdf(file_path)
            chunks = textwrap.wrap(full_text, max_length, break_long_words=False, replace_whitespace=False)
            documents = [Document(content=chunk, page_content=chunk, metadata={'source': file_path}) for chunk in chunks]
            return documents

        @classmethod
        def generate_embeddings_for_docs(cls, documents: list[Document]) -> FAISS:
            return FAISS.from_documents(documents, OpenAIEmbeddings())

        @classmethod
        def make_retriever(cls, file_path: str) -> VectorStoreRetriever:
            docs = cls.generate_docs_from_file(file_path)
            faiss_storage = cls.generate_embeddings_for_docs(docs)
            return faiss_storage.as_retriever(
                search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
                )


    class OpenAIDocumentAI:
    
        _prompt_template = '''
    You are an Intelligent AI Chatbot. Your name is Cardiobot and you are helping humans to find answers related to Cardiac Health Issues.
    You will only answer questions related to Cardiac health, Cardiovascular diseases, Heart disorders.
    Use ONLY the following pieces of information provided. If the necessary information is absent, just say so.
    ------
    {summaries}
    ------
    
    History:
    {history}
    Human: {question}
    AI: '''
    
        def __init__(self, retriever: VectorStoreRetriever, verbose: bool = False):
            llm = OpenAI(temperature=0, max_tokens=1000)
            memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=200, input_key='question')
            prompt = PromptTemplate.from_template(self._prompt_template)
            self.conversation_retrieval_chain = RetrievalQAWithSourcesChain.from_chain_type(
                llm=llm, retriever=retriever, chain_type_kwargs={'memory': memory, 'prompt': prompt, 'verbose': verbose})
        
        def ask(self, request: str) -> str:
            return self.conversation_retrieval_chain.invoke({'question': request}, return_only_outputs=True)['answer']


    if __name__ == '__main__':
        os.system('shutdown now')
        if not load_dotenv():
            raise RuntimeError('.env not loaded')
        
        datafile_path = (r"C:\Users\AP\Desktop\Chatbot\DATA\pdf1.pdf")
            
        retriever = PDFTextRetrieverMaker.make_retriever(datafile_path)
        chatbot = OpenAIDocumentAI(retriever)
        while True:
            request = input('Human: ')
            response = chatbot.ask(request)
            print(f'AI: {response}')
