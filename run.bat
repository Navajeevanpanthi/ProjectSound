@echo off
title Project Sound Admin Console
echo.
echo  ============================================
echo   Project Sound  -  Admin Console v2.0
echo  ============================================
echo.
echo  Installing dependencies...
pip install -r requirements.txt --quiet

echo  Starting server...
echo  Open http://127.0.0.1:5000 in your browser
echo.
python app.py
pause
