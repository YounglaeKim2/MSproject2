@echo off
echo Starting NewCompatibility Frontend (Port 3003)...
cd /d "c:\workspace\MSproject2\NewCompatibility\frontend"

echo Installing dependencies if needed...
if not exist "node_modules" (
    echo Installing npm packages...
    npm install
)

echo Setting port to 3003...
set PORT=3003

echo Starting React development server...
npm start

pause
