import time
start_time = time.time()
import asyncio
from fastapi import FastAPI, Depends
from app.models.schema import RunRequest, RunResponse
from app.services.pdf_utils import download_pdf_text
from app.services.rag_engine import build_rag_chain
from app.services.auth import verify_bearer_token
import_time = time.time()-start_time
print(f"the import time is {import_time}")
time2 = time.time()
app = FastAPI()


def batch_questions(questions, n_batches=5):
    """
    Split questions into exactly n_batches (default 5) in approximately equal size batches.
    """
    total = len(questions)
    batch_size = total // n_batches
    remainder = total % n_batches
    batches = []
    start = 0
    for i in range(n_batches):
        end = start + batch_size + (1 if i < remainder else 0)
        batches.append(questions[start:end])
        start = end
    return batches

@app.post("/hackrx/run", response_model=RunResponse)

async def hackrx_run(request: RunRequest, _auth=Depends(verify_bearer_token)):
    DELIMITER = "|||"

    text = download_pdf_text(request.documents)
    chain = build_rag_chain(text)
    pdf_and_chain_time = time.time()-time2
    print(f"the pdf time is :{pdf_and_chain_time}")
    async def ask_question(batch):
        print(f"asking questions {batch}")
        start_time2= time.time()
        prompt = (
            f"Answer each of the following questions in two sentences: "
            f"First, give a simple, precise one-line answer. "
            f"Second, provide a one-line explanation. "
            f"Questions are separated by '{DELIMITER}'. "
            f"For output, strictly separate each answer by '{DELIMITER}'.\n\n"
            f"Questions: {DELIMITER.join(batch)}"
        )
        result = await chain.ainvoke({"query": prompt})
        time_to_ans_query = time.time()
        print(f"the time to ans 1 query is{time_to_ans_query-start_time2}")
        return [ans.strip() for ans in result["result"].split(DELIMITER)]
    batches = list(batch_questions(request.questions,5))
    batch_answers = await asyncio.gather(*(ask_question(batch) for batch in batches if batch))
    answers = [item for sublist in batch_answers for item in sublist]
    # all_answers = answers[:len(request.questions)]
    print("answers:", answers)
    return RunResponse(answers=answers)

# @app.get("/hackrx/run")
# async def status_check():
#     return {
#         "status": "ready",
#         "info": "Use POST to /hackrx/run to send questions and PDF URL."
#     }
