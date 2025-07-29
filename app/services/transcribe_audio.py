from pydub import AudioSegment
from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def convert_to_16k_mono(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format="wav")

def transcribe_audio(audio_path: str) -> str:
    converted_path = audio_path + "_16k.wav"
    convert_to_16k_mono(audio_path, converted_path)

    segments, _ = model.transcribe(converted_path, beam_size=5, language="en")
    transcription = " ".join([seg.text for seg in segments])
    return transcription.strip()