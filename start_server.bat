@echo off
echo VideoTranscript3 MCP Server Starter
echo ================================
echo.

REM Prüfe, ob Python-Umgebung existiert
if not exist ".venv" (
    echo Erstelle virtuelle Umgebung...
    call uv venv
    if errorlevel 1 (
        echo Fehler beim Erstellen der virtuellen Umgebung!
        pause
        exit /b 1
    )
)

REM Aktiviere virtuelle Umgebung und starte Server
echo Starte MCP Server...
call .venv\Scripts\python.exe mcp_server.py

REM Bei Fehler warten
if errorlevel 1 (
    echo.
    echo Fehler beim Starten des Servers!
    pause
)