from flask import Flask, request, jsonify
from weaviate.language_modeling import ChatOpenAI, ChatPromptTemplate, StrOutputParser
from weaviate.tools import PyPDFLoader, RecursiveCharacterTextSplitter
from weaviate.vectorization import OpenAIEmbeddings, Weaviate
from weaviate.retrieval import RunnableParallel, RunnablePassthrough
import weaviate

app = Flask(__name__)

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    query = data['query']

    loader = PyPDFLoader('../data/RobinsonAdvisory.pdf')
    contract = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunk = text_splitter.split_documents(contract)

    client = weaviate.Client(embedded_options=weaviate.EmbeddedOptions)
    vectorstore = Weaviate.from_documents(client=client,
                                          documents=chunk,
                                          embedding=OpenAIEmbeddings(),
                                          by_text=False)

    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    prompt_template = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Question: {question} 
    Context: {context} 
    Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    retrieval = RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    chain = retrieval | prompt | llm | StrOutputParser()

    docs = vectorstore.similarity_search(query, k=3)
    answer = chain.run(input_documents=docs, question=query)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
