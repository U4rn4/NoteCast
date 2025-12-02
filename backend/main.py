from fastapi import FastAPI, UploadFile, File, Form
from transcriber import transcribe_audio, extract_audio, download_youtube_audio
from summarizer import summarize_text, extract_tasks
import os

app = FastAPI()

# Asegúrate de que las carpetas existen
os.makedirs("audios", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# Subir archivo local
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = os.path.join("audios", file.filename)
    with open(filename, "wb") as f:
        f.write(await file.read())
 
    # Si es vídeo, extraer audio
    if filename.endswith((".mp4", ".mov", ".mkv")):
        audio_path = os.path.join("audios", os.path.splitext(file.filename)[0] + ".wav")
        extract_audio(filename, audio_path)
    else:
        audio_path = filename

    text = transcribe_audio(audio_path)
    summary = summarize_text(text)
    tasks = extract_tasks(summary)

    return {"filename": file.filename, "summary": summary, "tasks": tasks}

# Procesar YouTube
@app.post("/youtube")
async def process_youtube(url: str = Form(...)):
    audio_path = download_youtube_audio(url)
    text = transcribe_audio(audio_path)
    summary = summarize_text(text)
    tasks = extract_tasks(summary)
    return {"url": url, "summary": summary, "tasks": tasks}
