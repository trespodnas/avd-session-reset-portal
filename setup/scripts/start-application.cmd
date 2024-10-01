@echo off
cd "C:\Program Files\avd-reset-portal"
call .venv\Scripts\activate.bat
waitress-serve --listen=localhost:5000 app:app