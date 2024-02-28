from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from langchain_openai import ChatOpenAI

import weaviate
from dotenv import load_dotenv,find_dotenv
from weaviate.embedded import EmbeddedOptions
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)
from langchain.schema.output_parser import StrOutputParser
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

import os

load_dotenv()

OPENAI_KEY=os.environ["OPENAI_API_KEY"]

file = '/home/kerod/Desktop/week_11/RAG-system-for-Contract-Q-A/data/Robinson Advisory.docx'

def data_loader(loaders):
    
    contract = loaders.load()

    return contract

def text_splitter(doc):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunk  = text_splitter.split_documents(doc)

    return chunk


def create_vectoreStore(doc):
    vectorStore =  Weaviate.from_documents(client =  client,
                                      documents= doc,
                                      embedding=OpenAIEmbeddings(),
                                      by_text = False)
    
    return vectorStore
    
def create_retriever(vectorstore):
    retriever = vectorstore.as_retriever()

    return retriever

def create_chian(retriever):
        # Define LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Define prompt template
    prompt_template = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Question: {question} 
    Context: {context} 
    Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)


    retrieval = RunnableParallel(
        {"context": retriever,  "question": RunnablePassthrough()} 
    )

    chain = retrieval | prompt | llm | StrOutputParser()

    return chain

def response(chain,query):

    return chain.invoke(query)



def main():
    loader = PyPDFLoader('/home/kerod/Desktop/week_11/RAG-system-for-Contract-Q-A/data/RobinsonAdvisory.pdf')
    data = data_loader(loader)
    chunk = text_splitter(data)
    vectorStore = create_vectoreStore(chunk)
    retriever = create_retriever(vectorStore)
    chain = create_chian(retriever)
    query = input("Enter query")
    answer = response(chain,query)

    print("Response: " + answer)

if __name__ == "__main__":
    main()