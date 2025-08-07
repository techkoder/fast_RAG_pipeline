from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

print("🔹 rag_engine is getting loadded")

llm_parameters={"chunk_size":1000,"chunk_overlap":200,"k":10,"temprature":0.4}

def build_rag_chain(text: str):
    # k_similar = get_search_k_similar(len(text))
    # 1. Split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=llm_parameters["chunk_size"], chunk_overlap=llm_parameters["chunk_overlap"])
    docs = text_splitter.create_documents([text])
    # 2. Setup embedding model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # 4. Load into Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding  
    )
    vector_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": llm_parameters["k"]})
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"
    )
    # 6. Build Retrieval QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_retriever
    )

    return qa_chain
