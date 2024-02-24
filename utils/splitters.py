from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings


def characterSplitter(doc, separator= "\n\n", chunk_size= 1000, chunk_overlap= 200, length_function= len, is_separator_regex= False):
    text_splitter = CharacterTextSplitter(
        separator= separator,
        chunk_size= chunk_size,
        chunk_overlap= chunk_overlap,
        length_function= length_function,
        is_separator_regex= is_separator_regex,
    )


    texts = text_splitter.split_documents(doc)
    
    return texts



def RecursiveSplitter(doc, chunk_size=1000, chunk_overlap=200, length_function=len, is_separator_regex=False):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        is_separator_regex=is_separator_regex,
    )


    texts = text_splitter.split_documents(doc)

    return texts

 
def SemanticSplitter(doc): 
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    docs = text_splitter.split_documents(doc)

    return docs
