from fastapi import FastAPI, Depends, HTTPException
from app.models.schema import RunRequest, RunResponse, AnswerItem
from app.services.pdf_utils import download_pdf_text
from app.services.rag_engine import build_rag_chain
from app.services.auth import verify_bearer_token

app = FastAPI()

@app.post("/hackrx/run", response_model=RunResponse)
async def hackrx_run(
    request: RunRequest,
    _auth=Depends(verify_bearer_token)
):
    try:
        text = download_pdf_text(str(request.documents))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"PDF download/parse failed: {str(e)}")
    

    chain = build_rag_chain(text)

    answers = []
    for q in request.questions:
        text = f"give ans in a single line and give precise answer. {q}"
        result = chain(text)
        ans = result["result"]
        sources = [doc.page_content[:300] for doc in result["source_documents"]]
        answers.append(AnswerItem(question=q, answer=ans, sources=sources))

    return RunResponse(answers=answers)

