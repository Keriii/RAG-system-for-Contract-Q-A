from fastapi import File, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from rag_pipeline import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    objective: str

def load_env_vars():
    load_dotenv()
    return os.environ["OPENAI_API_KEY"]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f'/home/kerod/Desktop/week_11/RAG-system-for-Contract-Q-A/backend/file/{file.filename}'
    with open(file_path, "wb+") as file_object:
        file_object.write(await file.read())
    return {"filename": file.filename}

@app.post("/query")
async def process_query(query: Query):
    OPENAI_KEY = load_env_vars()
    file_path = f'/home/kerod/Desktop/week_11/RAG-system-for-Contract-Q-A/backend/file/RobinsonAdvisory.pdf'
    loader = PyPDFLoader(file_path)
    data = data_loader(loader)
    chunk = text_splitter(data)
    vectorstore = create_vectoreStore(chunk)
    retriever = create_retriever(vectorstore)
    chain = create_chian(retriever)
    answer = response(chain, query.objective)
    return {"Answer": answer}