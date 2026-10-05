@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Open-RuntimeViewer.ps1" %*
exit /b %errorlevel%
