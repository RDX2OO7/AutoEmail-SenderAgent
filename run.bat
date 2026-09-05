@echo off
echo ===================================================
echo     AUTOMATED EMAIL SENDER & CERTIFICATE AGENT
echo ===================================================
echo.

:: Activate virtual environment if present
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: Run the full automated pipeline
python main.py

echo.
echo ===================================================
echo Pipeline execution finished!
echo ===================================================
pause
