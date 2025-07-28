from fastapi import FastAPI, Depends, HTTPException
from app.models.schema import RunRequest, RunResponse
from app.services.pdf_utils import download_pdf_text
from app.services.rag_engine import build_rag_chain
from app.services.auth import verify_bearer_token
import traceback

app = FastAPI()

@app.post("/hackrx/run", response_model=RunResponse)
async def hackrx_run(request: RunRequest, _auth=Depends(verify_bearer_token)):
    try:
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

    except Exception as e:
        print("❗ Error occurred:", e)
        traceback.print_exc()  # This is key
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
