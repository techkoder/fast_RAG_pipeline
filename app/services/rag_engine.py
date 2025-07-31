from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

import time
from google.api_core.exceptions import ResourceExhausted
print("🔹 rag_engine is getting loadded")
def build_rag_chain(text: str):
    # 1. Split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])

    # 2. Setup embedding model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # 3. Batch and embed with retries
    print(len(docs))
    batch_size = 200
    embedded_docs = []
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]

        retries = 3
        while retries:
            try:
                # embedding.embed_documents(texts)  # this just confirms it works
                embedded_docs.extend(batch)
                break
            except ResourceExhausted:
                print("[429] Rate limit hit. Retrying...")
                time.sleep(5)
                retries -= 1
            except Exception as e:
                print(f"Error embedding batch {i}: {e}")
                retries = 0

    # 4. Load into Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=embedded_docs,
        embedding=embedding  # ⬅️ this must be the embedding function
    )

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # 5. Setup Gemini 1.5 LLM
    llm = ChatGoogleGenerativeAI(
        model="learnlm-2.0-flash-experimental",
        temperature=0
    )

    # 6. Build Retrieval QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
