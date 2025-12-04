import whisper
from moviepy import VideoFileClip
import os
import yt_dlp
import uuid

# Cargar modelo Whisper
model_whisper = whisper.load_model("base")

# Transcribir audio
def transcribe_audio(audio_path):
    print(f"🎤 Iniciando transcripción de: {audio_path}")
    result = model_whisper.transcribe(audio_path, verbose=True)
    print(f"✅ Transcripción completada")
    return result["text"]

# Extraer audio de vídeo
def extract_audio(video_path, output_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path)
 
# Descargar vídeo de YouTube y extraer audio
def download_youtube_audio(url, output_folder="audios"):
    # Generar nombre único para el archivo
    unique_id = uuid.uuid4().hex[:8]
    
    # Configurar opciones de yt-dlp con estrategia anti-bloqueo mejorada
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': os.path.join(output_folder, f"youtube_{unique_id}"),
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [lambda d: print(f"📥 Descarga: {d.get('_percent_str', 'N/A')}") if d['status'] == 'downloading' else None],
        # Usar cliente de Android que es menos restrictivo
        'extractor_args': {
            'youtube': {
                'player_client': ['android_creator'],
            }
        },
        # Headers adicionales para evitar bloqueos
        'http_headers': {
            'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    # Descargar audio
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # El archivo resultante tendrá extensión .wav
            base_filename = ydl.prepare_filename(info)
            audio_path = os.path.splitext(base_filename)[0] + '.wav'
        
        return audio_path
    except Exception as e:
        raise Exception(f"Error al descargar el video de YouTube: {str(e)}")
