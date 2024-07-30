pip install venv

rd /s /q "venv"

python -m venv venv

#powershell -NoExit -Command "Set-ExecutionPolicy Unrestricted -Scope Process; Set-Location -Path '%~dp0'; .\venv\Scripts\Activate.ps1 ; pip install -r requirements.txt"

powershell -Command "Set-ExecutionPolicy Unrestricted -Scope Process; Set-Location -Path '%~dp0'; .\venv\Scripts\Activate.ps1 ; pip install -r requirements.txt"
