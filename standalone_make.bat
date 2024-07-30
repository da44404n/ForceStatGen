@echo off
setlocal
set bat_dir=%~dp0
set target_dir=%bat_dir%\subdir

call venv\Scripts\activate

pyinstaller -F --hidden-import "babel.numbers" --hidden-import "openpyxl.cell._writer" --upx-dir "C:\Program Files (x86)\upx-4.2.4-win64\upx.exe" --icon=./images/nypd.ico --add-data "images/nypd.ico;." --splash "images/nypdsplash.png" --onefile --noconsole --name ForceStatGen src/__main__.py

# powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('ForceStatGen.lnk'); $s.TargetPath=$pwd.Path + '\dist\ForceStatGen.exe'; $s.Save()"

deactivate