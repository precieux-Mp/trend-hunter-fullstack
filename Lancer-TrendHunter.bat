@echo off
cd /d "%~dp0"

echo Demarrage de Trend Hunter (Docker)...
start "" cmd /k "docker compose up"

echo Attente du demarrage du backend (25s)...
timeout /t 25 /nobreak

echo Ouverture du frontend...
start "" "frontend\index.html"

echo Termine. Trend Hunter est lance.
