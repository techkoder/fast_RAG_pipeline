import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

def build_rag_chain(text: str, persist_dir: str = "./storage/chroma_store"):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])
    # embeddings
    if os.getenv("GOOGLE_API_KEY"):
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

  # OpenAI embeddings still work
    else:
        llm = None
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vectorstore = Chroma.from_documents(docs, embedding, persist_directory=persist_dir)
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    chain = RetrievalQA.from_chain_type(
        llm=llm if llm else ChatGoogleGenerativeAI(model="gemini-pro", temperature=0) if False else llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain
