from fastapi import FastAPI, Depends
print("🔹 FastAPI loaded")
from app.models.schema import RunRequest, RunResponse
print("🔹 Models1 loaded")
from app.services.pdf_utils import download_pdf_text
print("🔹 Models1 loaded")
from app.services.rag_engine import build_rag_chain
print("🔹 Models1 loaded")
from app.services.auth import verify_bearer_token
print("🔹 Models1 loaded")

app = FastAPI()

@app.post("/hackrx/run", response_model=RunResponse)
async def hackrx_run(request: RunRequest, _auth=Depends(verify_bearer_token)):
    if request.status_code == 200:
        print("🔹 Request received")
    else:
        print("❗ Error occurred:", request.status_code)
        print("🔹 Request received")
        print("Documents:", request.documents)
        print("Questions:", request.questions)

        text = download_pdf_text(request.documents)
        print("🔹 PDF downloaded")

        chain = build_rag_chain(text)
        print("🔹 RAG chain built")

        answers = []
        for q in request.questions:
            result = chain(q)
            print("🔹 Question processed:", q)
            answers.append(result["result"])

        print("🔹 Final answers:", answers)
        return RunResponse(answers=answers)
