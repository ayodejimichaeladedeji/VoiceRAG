import os
import tempfile
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, Form

from app.services import embedding
from app.services.embedding import embed_and_store, preview_vectors
from app.services.transcribe_audio import transcribe_audio

router = APIRouter()

@router.post("/ask_text")
async def ask_question_with_text(question: str = Form(None)):
    if question:
        return JSONResponse({"question": question})
    else:
        return JSONResponse({"error": "No question provided"}, status_code=400)

@router.post("/ask_audio")
async def ask_question_with_audio(audio: UploadFile = File(None)):
    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        transcript = transcribe_audio(tmp_path)
        os.remove(tmp_path)

        return JSONResponse({"transcript": transcript})
    else:
        return JSONResponse({"error": "No audio provided"}, status_code=400)

@router.post("/upload_document")
async def upload_document(file: UploadFile):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return JSONResponse(status_code=400, content={"error": "Only PDF/DOCX files allowed"})

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = embed_and_store(tmp_path)
        return {"message": "File processed", "chunks": result["num_chunks"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(tmp_path)

@router.get("/test")
async def testtest():
    results = preview_vectors(['What are the projected impacts of climate change on wheat yields?'])
    return {"results": results}

#         # Pass transcript through RAG pipeline
#         # chunks = embed_and_retrieve(transcript)
#         # answer = generate_answer(transcript, chunks)
#         #  chunks = embed_and_retrieve(question)
#         #  answer = generate_answer(question, chunks)