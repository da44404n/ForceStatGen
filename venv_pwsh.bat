@echo off
powershell -NoExit -Command "Set-ExecutionPolicy Unrestricted -Scope Process; Set-Location -Path '%~dp0'; .\venv\Scripts\Activate.ps1"
