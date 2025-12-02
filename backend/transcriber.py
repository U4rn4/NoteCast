import whisper
from moviepy import VideoFileClip
import os
from pytube import YouTube

# Cargar modelo Whisper
model_whisper = whisper.load_model("base")

# Transcribir audio
def transcribe_audio(audio_path):
    result = model_whisper.transcribe(audio_path)
    return result["text"]

# Extraer audio de vídeo
def extract_audio(video_path, output_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path)
 
# Descargar vídeo de YouTube y extraer audio
def download_youtube_audio(url, output_folder="audios"):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = f"{yt.title}.mp4"
    video_path = os.path.join("videos", filename)
    stream.download(output_path="videos", filename=filename)
    
    audio_filename = f"{yt.title}.wav"
    audio_path = os.path.join(output_folder, audio_filename)
    extract_audio(video_path, audio_path)
    return audio_path
