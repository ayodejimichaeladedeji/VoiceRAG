import os
import tempfile

from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, Form

from services.rag_pipeline import answer_with_rag
from services.transcribe_audio import transcribe_audio
from services.embedding import embed_and_store, preview_vectors

router = APIRouter()

@router.post("/ask_text")
async def ask_question_with_text(question: str = Form(...)):
    try:
        if question:
            answer = answer_with_rag(question)
            return {"answer": answer}
        else:
            return JSONResponse({"error": "No question provided"}, status_code=400)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/ask_audio")
async def ask_question_with_audio(audio: UploadFile = File(...)):
    try:
        if audio:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(await audio.read())
                tmp_path = tmp.name

            transcript_question = transcribe_audio(tmp_path)
            os.remove(tmp_path)
            answer = answer_with_rag(transcript_question)
            return {"answer": answer}
        else:
            return JSONResponse({"error": "No audio provided"}, status_code=400)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/upload_document")
async def upload_document(file: UploadFile = File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return JSONResponse(status_code=400, content={"error": "Only PDF/DOCX files allowed"})

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        result = embed_and_store(tmp_path)
        os.remove(tmp_path)
        return {"message": "File processed", "chunks": result["num_chunks"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(tmp_path)

@router.get("/test")
async def testtest():
    results = preview_vectors(['By how much did the cost of solar PV electricity drop between 2021 and 2024?'])
    return {"results": results}