import os
from pathlib import Path
import whisper
import json
from tqdm import tqdm

def setup_directories():
    """Erstellt die benötigte Ordnerstruktur."""
    base_dir = Path("output")
    dirs = {
        "videos": base_dir / "videos",
        "transcripts": base_dir / "transcripts",
        "results": base_dir / "results"
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs

def transcribe_audio(audio_path, dirs):
    """Transkribiert eine Audiodatei mit Whisper."""
    print(f"\nTranskribiere: {audio_path}")
    
    # Lade das Modell (wird beim ersten Mal heruntergeladen)
    model = whisper.load_model("base")
    
    try:
        # Transkribiere die Datei
        result = model.transcribe(str(audio_path))
        return result["text"]
    except Exception as e:
        print(f"Fehler bei der Transkription: {str(e)}")
        return None

def create_summary_prompt(transcript):
    """Erstellt den Prompt für die Zusammenfassung."""
    with open("prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    return prompt_template.replace("{transcript}", transcript)

def save_results(audio_path, transcript, summary_prompt, dirs):
    """Speichert Transkript und Zusammenfassungs-Prompt."""
    filename = audio_path.stem  # Name ohne Endung
    
    # Speichere Transkript
    transcript_path = dirs['transcripts'] / f"{filename}_transcript.txt"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Transkript gespeichert: {transcript_path}")
    
    # Speichere Prompt
    prompt_path = dirs['results'] / f"{filename}_summary_prompt.txt"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(summary_prompt)
    print(f"Zusammenfassungs-Prompt gespeichert: {prompt_path}")

def process_videos_folder():
    """Verarbeitet alle Audiodateien im videos-Ordner."""
    # Erstelle Ordnerstruktur
    dirs = setup_directories()
    
    # Finde alle Audiodateien
    audio_files = []
    for ext in [".wav", ".mp3", ".m4a"]:
        audio_files.extend(dirs['videos'].glob(f"*{ext}"))
    
    if not audio_files:
        print("Keine Audiodateien gefunden!")
        return
    
    print(f"\nGefundene Audiodateien: {len(audio_files)}")
    
    # Verarbeite jede Datei
    for audio_path in audio_files:
        print(f"\nVerarbeite: {audio_path}")
        
        # Prüfe ob bereits transkribiert
        transcript_path = dirs['transcripts'] / f"{audio_path.stem}_transcript.txt"
        if transcript_path.exists():
            print("Transkript existiert bereits, überspringe...")
            continue
        
        # Transkribiere
        transcript = transcribe_audio(audio_path, dirs)
        if transcript:
            # Erstelle Zusammenfassungs-Prompt
            summary_prompt = create_summary_prompt(transcript)
            
            # Speichere Ergebnisse
            save_results(audio_path, transcript, summary_prompt, dirs)
        else:
            print("Transkription fehlgeschlagen!")

if __name__ == "__main__":
    process_videos_folder()