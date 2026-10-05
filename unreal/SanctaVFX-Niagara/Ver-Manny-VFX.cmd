@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Open-MannyLab.ps1" %*
if errorlevel 1 pause
