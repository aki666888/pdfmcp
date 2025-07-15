@echo off
echo ============================================================
echo Testing PharmaCare MACS Form Filler
echo ============================================================

echo.
echo 1. Testing Simple Form...
start python simple_form.py

echo.
echo 2. Testing Form Overlay (requires form image)...
timeout /t 3 >nul
start python form_filler.py "Test Patient" "headache" "1234567890" "(250) 555-0123"

echo.
echo 3. Claude Desktop Configuration:
echo    Location: C:\Users\info0\AppData\Roaming\Claude\claude_desktop_config.json
echo    Server Name: pharmacare-form
echo.
echo    Try these commands in Claude Desktop:
echo    - "Open the pharmacy form"
echo    - "Fill MACS form for John Doe with headache"
echo    - "Quick fill UTI form for Jane Smith"
echo.
echo ============================================================
pause