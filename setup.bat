@echo off
echo ============================================================
echo PharmaCare MACS Form Filler Setup
echo ============================================================

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Install required packages
echo Installing required packages...
pip install pillow tk mcp

:: Install MCPShell (optional - for command line usage)
echo.
echo Installing MCPShell for command line usage...
pip install mcpshell

:: Create desktop shortcut
echo.
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\MACS Form Filler.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%~dp0form_filler.py'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,1'; $Shortcut.Save()"

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Usage Options:
echo 1. Double-click "MACS Form Filler" on desktop
echo 2. Use with Claude Desktop (add to claude_desktop_config.json)
echo 3. Command line: python form_filler.py "Patient Name" "condition"
echo.
echo To use with Claude Desktop, add this to your config:
echo.
echo "pharmacare-form": {
echo   "command": "python",
echo   "args": ["%~dp0mcp_server.py"]
echo }
echo.
pause