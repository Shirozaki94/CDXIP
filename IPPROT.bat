@echo off
cd /d D:\IPPROTECT
start /B /WAIT cmd.exe /c "python main.py"
timeout /t 10
