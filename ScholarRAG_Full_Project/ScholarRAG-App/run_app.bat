@echo off
title ScholarRAG - Multi-PDF Intelligence Assistant
cd /d "%~dp0"
echo ========================================================
echo   Starting ScholarRAG (Multi-PDF AI Assistant)...
echo ========================================================
echo.
call venv\Scripts\activate.bat
streamlit run app.py
pause
