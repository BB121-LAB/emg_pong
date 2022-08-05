@echo off
type pong.py > pong.pyw
pip3 install -r requirements.txt
pip3 install pyinstaller
pyinstaller --name="One Button Pong" --clean --onefile pong.pyw
del /f /q pong.pyw
