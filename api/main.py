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
        # Log request input
        print(f"Received documents={request.documents}, questions={request.questions}")

        # You might need to adapt this line to handle multiple docs properly
        text = download_pdf_text(str(request.documents))

        chain = build_rag_chain(text)

        answers = []
        for q in request.questions:
            prompt = f"give ans in a single line and give precise answer. {q}"
            result = chain(prompt)
            ans = result["result"]
            sources = [doc.page_content[:300] for doc in result["source_documents"]]
            answers.append(AnswerItem(question=q, answer=ans, sources=sources))

        return RunResponse(answers=answers)
    
    except Exception as e:
        print(f"Unhandled error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
