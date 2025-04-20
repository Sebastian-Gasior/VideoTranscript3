# VideoTranscript3

Ein Tool zur automatischen Verarbeitung von Video-Transkripten mit Claude Desktop Integration.

## Voraussetzungen

- Python 3.10 oder höher
- [uv](https://github.com/astral-sh/uv) für Paketmanagement
- [Claude Desktop](https://claude.ai/desktop) (als Administrator ausführen!)
- FFmpeg (für Video-Extraktion)

## Installation

1. Repository klonen:
```bash
git clone https://github.com/Sebastian-Gasior/VideoTranscript3.git
cd VideoTranscript3
```

2. Virtuelle Umgebung erstellen und Abhängigkeiten installieren:
```bash
uv venv
uv pip install -r requirements.txt
```

3. Claude Desktop konfigurieren:
   - Starte Claude Desktop als Administrator
   - Navigiere zu: `%APPDATA%/Claude/claude_desktop_config.json`
   - Die vollständige Datei "claude_desktop_config.json" findest du im Hauptverzeichnis.
   ```json
       "cwd": "C:\\DEIN_PFAD_ZU_DEISEM_PROJEKT\\VideoTranscript3",
   ```
   - Ersetze `C:\\DEIN_PFAD_ZU_DEISEM_PROJEKT\\VideoTranscript3` mit deinem tatsächlichen Pfad
   - Beispiel: `C:\\Users\\DeinName\\Documents\\GitHub\\VideoTranscript3`
   - Starte Claude Desktop neu

## Verzeichnisstruktur

```
VideoTranscript3/
├── output/
│   ├── videos/      # Heruntergeladene Videos
│   ├── results/     # Generierte Prompts
│   ├── processed/   # Von Claude verarbeitete Ergebnisse
│   └── transcripts/ # Extrahierte Transkripte
├── start_server.bat # Server-Startskript
├── download_videos.py
├── transcribe.py
└── mcp_server.py
```

## Verwendung

1. **Server starten:**
   - Doppelklick auf `start_server.bat` ODER
   - Im Terminal: `python mcp_server.py`

2. **Videos herunterladen und transkribieren:**
   ```bash
   python download_videos.py
   python transcribe.py
   ```

3. **Transkripte verarbeiten:**
   - Starte Claude Desktop als Administrator
   - Die Verbindung zum MCP Server wird automatisch hergestellt (grüner Punkt)
   - Die Prompts werden automatisch verarbeitet
   - Du findest die Ergebnisse im `output/processed` Verzeichnis

## Workflow

1. **Video-Download:**
   - `download_videos.py` lädt Videos herunter
   - Extrahiert Audio in WAV-Format
   - Speichert in `output/videos`

2. **Transkription:**
   - `transcribe.py` erstellt Transkripte
   - Generiert Prompts für Claude
   - Speichert in `output/results`

3. **Claude-Integration:**
   - `mcp_server.py` verbindet mit Claude Desktop
   - Verarbeitet Prompts automatisch
   - Speichert Ergebnisse in `output/processed`

## Wichtige Hinweise

- **Claude Desktop MUSS als Administrator ausgeführt werden!**
- Der MCP Server muss laufen, bevor du Claude Desktop startest
- Alle Ausgabedateien werden automatisch im `output` Verzeichnis organisiert
- Bei Problemen: Starte den Server neu und verbinde Claude Desktop erneut

## Fehlerbehebung

1. **Server startet nicht:**
   - Prüfe, ob alle Python-Pakete installiert sind
   - Aktiviere die virtuelle Umgebung
   - Prüfe auf Port-Konflikte

2. **Claude Desktop verbindet nicht:**
   - Starte als Administrator neu
   - Starte den Server neu
   - Prüfe die Konfigurationsdatei
   - Prüfe den Pfad in `claude_desktop_config.json`
   - Prüfe die Capabilities in der Konfigurationsdatei

3. **Prompts werden nicht verarbeitet:**
   - Prüfe die Debug-Ausgaben im Terminal
   - Prüfe die Dateiberechtigungen
   - Prüfe die Verzeichnisstruktur