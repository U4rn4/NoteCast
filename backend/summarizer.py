from transformers import pipeline

# Pipeline para resumir
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]["summary_text"]

# Extraer tareas/puntos clave simples
def extract_tasks(summary):
    return [line for line in summary.split(".") if "deber" in line.lower() or "hacer" in line.lower()]
