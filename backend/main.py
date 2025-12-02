from fastapi import FastAPI, UploadFile, File
from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline
import os

app = FastAPI()

# Cargar modelos
model_whisper = whisper.load_model("base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Funciones
def extract_audio(video_path, output_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path)

def transcribe_audio(audio_path):
    result = model_whisper.transcribe(audio_path)
    return result["text"]

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]["summary_text"]

def extract_tasks(summary):
    return [line for line in summary.split(".") if "deber" in line.lower() or "hacer" in line.lower()]

# Endpoints
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = f"audios/{file.filename}"
    with open(filename, "wb") as f:
        f.write(await file.read())

    # Si es vídeo, extraer audio
    if filename.endswith((".mp4", ".mov", ".mkv")):
        audio_path = f"audios/{os.path.splitext(file.filename)[0]}.wav"
        extract_audio(filename, audio_path)
    else:
        audio_path = filename

    text = transcribe_audio(audio_path)
    summary = summarize_text(text)
    tasks = extract_tasks(summary)

    return {"filename": file.filename, "summary": summary, "tasks": tasks}
