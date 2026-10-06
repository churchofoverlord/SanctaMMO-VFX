@echo off
if not exist "%~dp0Evidence\MannyFullReview\galeria.html" (
  echo A galeria completa ainda esta a ser preparada.
  pause
  exit /b 1
)
start "" "%~dp0Evidence\MannyFullReview\galeria.html"
