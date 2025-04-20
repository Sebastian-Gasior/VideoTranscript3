import os
import sys
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server import stdio
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions, Server

# Create an MCP server
mcp = FastMCP("VideoTranscript3")

# Absolute Verzeichnisse
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = BASE_DIR / "output" / "results"
PROCESSED_DIR = BASE_DIR / "output" / "processed"
TRANSCRIPTS_DIR = BASE_DIR / "output" / "transcripts"

def debug_log(message: str):
    """Debug-Ausgabe mit Zeitstempel"""
    print(f"[DEBUG] {message}", file=sys.stderr)

def ensure_directories():
    """Stelle sicher, dass die Verzeichnisse existieren"""
    debug_log("Erstelle Verzeichnisse...")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    debug_log("Verzeichnisse erstellt/überprüft")

@mcp.tool()
def process_prompt_file() -> dict:
    """
    Verarbeitet automatisch die vorhandene Prompt-Datei.
    Liest den Inhalt, verarbeitet ihn und speichert das Ergebnis.

    Returns:
        dict: Status und Pfad der gespeicherten Datei
    """
    debug_log("Starte process_prompt_file()")
    ensure_directories()
    
    # Finde die Prompt-Datei
    prompt_files = list(RESULTS_DIR.glob("*_prompt.txt"))
    debug_log(f"Gefundene Prompt-Dateien: {[str(f) for f in prompt_files]}")
    
    if not prompt_files:
        debug_log("Keine Prompt-Datei gefunden!")
        raise ValueError("Keine Prompt-Datei gefunden")
    
    prompt_file = prompt_files[0]
    content = prompt_file.read_text(encoding="utf-8")
    debug_log(f"Prompt-Datei gelesen: {prompt_file.name}")
    
    # Erstelle den Ausgabepfad
    output_file = PROCESSED_DIR / prompt_file.name.replace("_prompt.txt", "_result.txt")
    debug_log(f"Ausgabepfad erstellt: {output_file}")
    
    return {
        "prompt_file": str(prompt_file.absolute()),
        "content": content,
        "output_file": str(output_file.absolute())
    }

@mcp.tool()
def save_prompt_result(content: str, filename: str) -> dict:
    """
    Speichert das Ergebnis eines verarbeiteten Prompts in einer Datei.

    Args:
        content (str): Der zu speichernde Inhalt
        filename (str): Name der Zieldatei

    Returns:
        dict: Status und Pfad der gespeicherten Datei
    """
    debug_log(f"Speichere Prompt-Ergebnis in: {filename}")
    ensure_directories()
    filepath = PROCESSED_DIR / filename.replace("_prompt.txt", "_result.txt")
    filepath.write_text(content, encoding="utf-8")
    debug_log(f"Ergebnis gespeichert in: {filepath}")
    return {"success": True, "filepath": str(filepath.absolute())}

@mcp.tool()
def read_prompt_file(filename: str) -> dict:
    """
    Liest den Inhalt einer Prompt-Ergebnisdatei.

    Args:
        filename (str): Name der zu lesenden Datei

    Returns:
        dict: Status und Inhalt der Datei
    """
    debug_log(f"Lese Prompt-Datei: {filename}")
    ensure_directories()
    filepath = RESULTS_DIR / filename
    if not filepath.exists():
        raise ValueError(f"Datei nicht gefunden: {filepath.absolute()}")
    
    content = filepath.read_text(encoding="utf-8")
    debug_log(f"Datei erfolgreich gelesen: {filepath}")
    return {"success": True, "content": content, "filepath": str(filepath.absolute())}

@mcp.prompt()
def auto_process_prompt() -> str:
    """
    Generiert automatisch einen Prompt zur Verarbeitung der vorhandenen Datei.
    """
    debug_log("Generiere automatischen Prompt")
    result = process_prompt_file()
    prompt = f"""Bitte verarbeite die folgende Datei gemäß den enthaltenen Anweisungen:

Datei: {result['prompt_file']}

Inhalt:
{result['content']}

Speichere das Ergebnis in: {result['output_file']}"""
    debug_log("Prompt generiert")
    return prompt

async def main():
    """Hauptfunktion"""
    try:
        ensure_directories()
        debug_log("MCP Server wird gestartet...")
        debug_log(f"Verzeichnisse:")
        debug_log(f"- Results: {RESULTS_DIR.absolute()}")
        debug_log(f"- Processed: {PROCESSED_DIR.absolute()}")
        
        async with stdio.stdio_server() as (read_stream, write_stream):
            debug_log("Server-Verbindung hergestellt")
            server = Server(mcp)
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="VideoTranscript3",
                    server_version="1.0.0",
                    capabilities={
                        "notifications": NotificationOptions().__dict__,
                        "experimental": {}
                    }
                )
            )
            debug_log("Server beendet")
    except Exception as e:
        debug_log(f"Fehler: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        debug_log("Server durch Benutzer beendet")
    except Exception as e:
        debug_log(f"Unerwarteter Fehler: {str(e)}")
        sys.exit(1)