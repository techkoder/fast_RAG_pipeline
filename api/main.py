from fastapi import FastAPI, Depends
from app.models.schema import RunRequest, RunResponse
from app.services.pdf_utils import download_pdf_text
from app.services.rag_engine import build_rag_chain
from app.services.auth import verify_bearer_token

app = FastAPI()

@app.post("/hackrx/run", response_model=RunResponse)
async def hackrx_run(request: RunRequest, _auth=Depends(verify_bearer_token)):
    text = download_pdf_text(request.documents)
    chain = build_rag_chain(text)
    answers = []
    for q in request.questions:
        optimized_query = f"Pls give a precise answer in a single line. {q}"
        result =await chain.ainvoke({"query": optimized_query})
        answers.append(result["result"])
    print("answers:", answers)
    return RunResponse(answers=answers)

@app.get("/hackrx/run")
async def status_check():
    return {
        "status": "ready",
        "info": "Use POST to /hackrx/run to send questions and PDF URL."
    }
