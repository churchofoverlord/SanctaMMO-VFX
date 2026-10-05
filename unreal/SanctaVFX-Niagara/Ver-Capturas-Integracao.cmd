@echo off
if not exist "%~dp0Evidence\RuntimeReview\galeria.html" (
    echo A galeria ainda nao foi gerada neste laboratorio.
    pause
    exit /b 1
)
start "" "%~dp0Evidence\RuntimeReview\galeria.html"
