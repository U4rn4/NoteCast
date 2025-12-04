from transformers import pipeline

# Pipeline para resumir con modelo más pequeño y estable
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except:
    summarizer = None
    print("⚠️ No se pudo cargar el modelo de resumen. Usando resumen simple.")

def summarize_text(text):
    words = text.split()
    
    # Si el texto es muy corto, devolver directamente
    if len(words) < 50:
        return text
    
    # Si no hay modelo disponible, hacer resumen extractivo simple
    if summarizer is None:
        # Tomar las primeras 200 palabras como resumen
        sentences = text.split('.')
        summary_sentences = []
        word_count = 0
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if word_count + sentence_words > 200:
                break
            summary_sentences.append(sentence)
            word_count += sentence_words
        return '. '.join(summary_sentences) + '.'
    
    # Intentar con el modelo
    try:
        # Limitar a 1024 tokens (aproximadamente 800 palabras)
        if len(words) > 800:
            text = ' '.join(words[:800])
        
        # Usar parámetros más conservadores
        max_len = min(100, len(words) // 4)
        min_len = min(30, max_len // 2)
        
        result = summarizer(
            text, 
            max_length=max_len, 
            min_length=min_len, 
            do_sample=False,
            truncation=True,
            clean_up_tokenization_spaces=True
        )
        
        summary = result[0]["summary_text"]
        print(f"✅ Resumen completado")
        return summary
        
    except Exception as e:
        print(f"⚠️ Error con modelo de resumen: {e}")
        print("📝 Usando resumen extractivo...")
        
        # Fallback: resumen extractivo (primeras oraciones importantes)
        sentences = text.split('.')
        # Tomar primeras 5-10 oraciones o hasta 200 palabras
        summary_sentences = []
        word_count = 0
        for sentence in sentences[:15]:
            sentence = sentence.strip()
            if not sentence:
                continue
            sentence_words = len(sentence.split())
            if word_count + sentence_words > 200:
                break
            summary_sentences.append(sentence)
            word_count += sentence_words
        
        return '. '.join(summary_sentences) + '.' if summary_sentences else text[:500] + "..."

# Extraer tareas/puntos clave simples
def extract_tasks(summary):
    return [line for line in summary.split(".") if "deber" in line.lower() or "hacer" in line.lower()]
