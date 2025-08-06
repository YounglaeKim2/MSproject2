@echo off
echo Starting NewCompatibility Backend Server (Port 8003)...
cd /d "c:\workspace\MSproject2\NewCompatibility\backend"

echo Installing dependencies...
pip install -r requirements.txt

echo Starting server...
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

pause
