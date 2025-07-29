import os
import tempfile

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydub import AudioSegment

from app.services.transcribe_audio import transcribe_audio

router = APIRouter()

@router.post("/ask_text")
async def ask_question_with_text(question: str = Form(None)):
    if question:
        return JSONResponse({"question": question})
    else:
        return JSONResponse({"error": "No question provided"}, status_code=400)

def convert_to_16k_mono(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format="wav")

@router.post("/ask_audio")
async def ask_question_with_audio(audio: UploadFile = File(None)):
    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        # 2. Convert audio to 16kHz mono WAV
        converted_path = tmp_path + "_16k.wav"
        convert_to_16k_mono(tmp_path, converted_path)

        transcript = transcribe_audio(tmp_path)
        os.remove(tmp_path)

        return JSONResponse({"transcript": transcript})
    else:
        return JSONResponse({"error": "No audio provided"}, status_code=400)


#         # Pass transcript through RAG pipeline
#         # chunks = embed_and_retrieve(transcript)
#         # answer = generate_answer(transcript, chunks)
#         #  chunks = embed_and_retrieve(question)
#         #  answer = generate_answer(question, chunks)