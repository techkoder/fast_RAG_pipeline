from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from app.services.parameter_selection import select_llm_parameters
import os

print("🔹 rag_engine is getting loadded")

def read_metadata():
    """Read metadata from meta_data.txt and extract pages, words, and sections"""
    metadata_path = "/tmp/meta_data.txt"
    
    pages = 0
    words = 0
    sections = 0
    
    try:
        with open(metadata_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('Number of Pages:'):
                    pages = int(line.split(':')[1].strip())
                elif line.startswith('Number of Words:'):
                    words = int(line.split(':')[1].strip())
                elif line.startswith('Number of Sections:'):
                    sections = int(line.split(':')[1].strip())
    except FileNotFoundError:
        print("Warning: meta_data.txt not found, using default values")
        pages, words, sections = 100, 50000, 50
    except Exception as e:
        print(f"Error reading metadata: {e}, using default values")
        pages, words, sections = 100, 50000, 50
    
    return pages, words, sections



def build_rag_chain(text: str):
    # Read metadata and get parameters
    pages, words, sections = read_metadata()
    print(f"📊 Metadata loaded - Pages: {pages}, Words: {words}, Sections: {sections}")
    llm_parameters = select_llm_parameters(pages, words, sections)
    # k_similar = get_search_k_similar(len(text))
    # 1. Split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=llm_parameters["chunk_size"], chunk_overlap=llm_parameters["overlap"])
    docs = text_splitter.create_documents([text])
    # 2. Setup embedding model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # 4. Load into Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding  
    )
    vector_retriever = vectorstore.as_retriever(
        search_type="mmr", 
        search_kwargs={
            "k": 8,
            "fetch_k": 20,
            "lambda_mult": 0.35
        }
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=1
    )
    # 6. Build Retrieval QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_retriever
    )

    return qa_chain
