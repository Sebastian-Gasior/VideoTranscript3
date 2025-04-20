import os
from pathlib import Path
import subprocess
import sys
import glob
import certifi
import ssl
from yt_dlp import YoutubeDL

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

def read_video_urls(filename):
    """Liest Video-URLs aus einer Textdatei."""
    if not os.path.exists(filename):
        print(f"Fehler: Die Datei {filename} existiert nicht!")
        return []
    
    urls = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def download_video(url, output_dir):
    """Download ein Video von der angegebenen URL"""
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True  # SSL-Zertifikatsprüfung deaktivieren
    }
    
    try:
        with YoutubeDL(options) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Fehler beim Download:\n{str(e)}")
        return False

def check_ffmpeg():
    """Überprüft die FFmpeg-Installation."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("FFmpeg ist korrekt installiert!")
            return True
        else:
            print("FFmpeg wurde nicht gefunden!")
            return False
    except Exception as e:
        print(f"Fehler bei der FFmpeg-Überprüfung: {str(e)}")
        return False

def main():
    # FFmpeg-Check
    if not check_ffmpeg():
        print("Bitte stellen Sie sicher, dass FFmpeg korrekt installiert ist!")
        sys.exit(1)
    
    # Erstelle Ordnerstruktur
    dirs = setup_directories()
    print(f"Ausgabeverzeichnis für Videos: {dirs['videos'].absolute()}")
    
    # Lese URLs
    urls = read_video_urls("video.txt")
    
    if not urls:
        print("Keine URLs gefunden!")
        return
    
    print(f"Gefundene URLs: {len(urls)}")
    
    # Verarbeite jede URL
    erfolge = 0
    for url in urls:
        print(f"\nVerarbeite URL: {url}")
        if download_video(url, dirs['videos']):
            erfolge += 1
            print("\nStarte Transkription...")
            try:
                subprocess.run(['python', 'transcribe.py'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Fehler bei der Transkription: {str(e)}")
    
    print(f"\nZusammenfassung: {erfolge} von {len(urls)} Downloads erfolgreich.")

if __name__ == "__main__":
    main()