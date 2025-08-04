from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.retrievers import BM25Retriever, EnsembleRetriever

print("🔹 rag_engine is getting loadded")
def get_search_k_similar(text_length):
    if text_length < 150000:
        return 3
    elif text_length < 750000:
        return 7
    else:
        return 10

def get_search_k_lexical(text_length):
    if text_length < 150000:
        return 2
    elif text_length < 750000:
        return 4
    else:
        return 7 

def build_rag_chain(text: str):
    k_similar = get_search_k_similar(len(text))
    # 1. Split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])
    # 2. Setup embedding model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # 4. Load into Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding  
    )
    vector_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k_similar})
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"
    )
    # 6. Build Retrieval QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_retriever
    )

    return qa_chain
