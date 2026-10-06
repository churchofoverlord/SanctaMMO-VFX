@echo off
if not exist "%~dp0Evidence\MannyReview\galeria.html" (
  echo A galeria Manny ainda nao foi gerada. Consultar MANNY_VFX.md.
  pause
  exit /b 1
)
start "" "%~dp0Evidence\MannyReview\galeria.html"
