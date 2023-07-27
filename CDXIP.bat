@echo off
cd /d D:\CDXIP
start /B /WAIT cmd.exe /c "python main.py"
timeout /t 10
