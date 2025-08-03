from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

print("🔹 rag_engine is getting loadded")
def build_rag_chain(text: str):
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
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 8})
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    )

    # 6. Build Retrieval QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa_chain
