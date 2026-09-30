@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Unreal-Lab.ps1" -Action Prepare %*
exit /b %errorlevel%
