from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def transcribe_audio(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path, beam_size=5, language="en")
    transcription = " ".join([seg.text for seg in segments])
    return transcription.strip()