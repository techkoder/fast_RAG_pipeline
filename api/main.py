from fastapi import FastAPI, Depends, HTTPException
from app.models.schema import RunRequest, RunResponse
from app.services.pdf_utils import download_pdf_text
from app.services.rag_engine import build_rag_chain
from app.services.auth import verify_bearer_token
import traceback

app = FastAPI()

@app.post("/hackrx/run", response_model=RunResponse)
async def hackrx_run(
    request: RunRequest,
    _auth=Depends(verify_bearer_token)
):
    try:
        print(f"Received request: {request.questions}")
        text = download_pdf_text(str(request.documents))
        chain = build_rag_chain(text)

        answers = []
        for q in request.questions:
            prompt = f"give ans in a single line and give precise answer. {q}"
            result = chain(prompt)
            ans = result["result"]
            answers.append(ans)  # no sources

        return RunResponse(answers=answers)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
