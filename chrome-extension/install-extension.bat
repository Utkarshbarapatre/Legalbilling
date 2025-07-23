@echo off
echo Legal Billing Email Summarizer - Chrome Extension Installer
echo.
echo This will help you install the Chrome extension.
echo.
echo Step 1: Make sure Chrome is installed
echo Step 2: Open Chrome and go to chrome://extensions/
echo Step 3: Enable "Developer mode" (toggle in top right)
echo Step 4: Click "Load unpacked" and select this folder:
echo %~dp0
echo.
echo Press any key to open Chrome extensions page...
pause >nul
start chrome://extensions/
echo.
echo Now:
echo 1. Enable Developer mode
echo 2. Click "Load unpacked"
echo 3. Select this folder: %~dp0
echo 4. Ignore any icon warnings
echo.
pause
