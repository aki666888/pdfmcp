@echo off
echo Installing MCP dependencies for PharmaCare Form...
echo.

"C:\Program Files\Python312\python.exe" -m pip install --upgrade pip
"C:\Program Files\Python312\python.exe" -m pip install mcp pillow

echo.
echo Installation complete!
echo.
echo To restart Claude Desktop:
echo 1. Close Claude Desktop completely (check system tray)
echo 2. Start Claude Desktop again
echo 3. Look for the tools icon in the bottom toolbar
echo 4. Click it to see connected MCP servers
echo.
pause