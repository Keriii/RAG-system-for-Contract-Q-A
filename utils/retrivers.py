import cohere
import weaviate
from langchain.vectorstores import Weaviate
from weaviate.embedded import EmbeddedOptions
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain_community.document_loaders import TextLoader


# template = """Answer the question based only on the following context:

# {context}

# Question: {question}
# """
# prompt = ChatPromptTemplate.from_template(template)
# model = ChatOpenAI()


# def format_docs(docs):
#     return "\n\n".join([d.page_content for d in docs])


# chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | model
#     | StrOutputParser()
# )

# chain.invoke("What did the president say about technology?")

# client = weaviate.Client(embedded_options=EmbeddedOptions)
# vectorstore = Weaviate.from_documents(client =  client,
#                                       documents= chunk,
#                                       embedding=OpenAIEmbeddings(),
#                                       by_text = False)





def vectoreStoreBacked(doc, embedding = OpenAIEmbeddings()):

    client = weaviate.Client(embedded_options=EmbeddedOptions)
    db = Weaviate.from_documents(client =  client,
                                      documents= doc,
                                      embedding=embedding,
                                      by_text = False)

    # retriever = db.as_retriever()
    retriever = db.as_retriever(
        search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
    )

    return retriever


def multiQuery(doc, embedding= OpenAIEmbeddings()):
    

    client = weaviate.Client(embedded_options=EmbeddedOptions)
    db = Weaviate.from_documents(client =  client,
                                      documents= doc,
                                      embedding=embedding,
                                      by_text = False)
    llm = ChatOpenAI(temperature=0)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(), llm=llm
    )

    # Set logging for the queries
    # import logging

    # logging.basicConfig()
    # logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

    # unique_docs = retriever_from_llm.get_relevant_documents(query=question)
    return retriever_from_llm



def baseRetriver(func):
    def wrapper(*args, **kwargs):
        retriever = FAISS.from_document(OpenAIEmbeddings()).as_retriever()

        return func(*args, **kwargs)
    return wrapper



# @baseRetriver
def compressorContext(doc, embedding= OpenAIEmbeddings()):

    client = weaviate.Client(embedded_options=EmbeddedOptions)
    db = Weaviate.from_documents(client =  client,
                                      documents= doc,
                                      embedding=embedding,
                                      by_text = False)

    retriever = db.as_retriever()
    # retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever()
    embeddings = OpenAIEmbeddings()
    embeddings_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=embeddings_filter, base_retriever=retriever
    )
    return compression_retriever



def compressorEmbeding(doc, embedding = OpenAIEmbeddings()):
    client = weaviate.Client(embedded_options=EmbeddedOptions)
    db = Weaviate.from_documents(client =  client,
                                      documents= doc,
                                      embedding=embedding,
                                      by_text = False)

    retriever = db.as_retriever()
    # retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever()
    embeddings = OpenAIEmbeddings()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0, separator=". ")
    redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
    relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)
    pipeline_compressor = DocumentCompressorPipeline(
        transformers=[splitter, redundant_filter, relevant_filter]
    )

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline_compressor, base_retriever=retriever
    )

    return compression_retriever


def reranker ():

    co = cohere.Client('{apiKey}')

    query = 'What is the capital of the United States?'
    docs = ['Carson City is the capital city of the American state of Nevada.',
        'The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.',
        'Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district. ',
        'Capital punishment (the death penalty) has existed in the United States since before the United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.'
        ]
    results = co.rerank(query=query, documents=docs, top_n=3, model='rerank-english-v2.0')