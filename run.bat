@echo off
title  Launching Thyroid App 

Clear the screen
cls

:: Run Streamlit
echo Launching Streamlit...
streamlit run main.py

echo.
echo Streamlit has exited. Press any key to close this window.
pause >nul
