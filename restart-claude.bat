@echo off
echo ============================================================
echo Restarting Claude Desktop with MCP Servers
echo ============================================================

echo Stopping Claude Desktop...
taskkill /F /IM "Claude.exe" >nul 2>&1
timeout /t 3 >nul

echo Starting Claude Desktop...
start "" "C:\Users\info0\AppData\Local\AnthropicClaude\claude.exe"

echo.
echo ============================================================
echo Claude Desktop is restarting!
echo ============================================================
echo.
echo After Claude opens:
echo 1. Look for the tools icon (🔨) in the bottom toolbar
echo 2. Click it to see connected MCP servers
echo 3. You should see "pharmacare-form" in the list
echo.
echo Test commands:
echo - "test pharmacare"
echo - "open the pharmacy form"
echo - "open form for John Doe"
echo.
echo If pharmacare-form doesn't appear:
echo - Check logs at: C:\Users\info0\AppData\Roaming\Claude\logs\
echo - Look for mcp-server-pharmacare-form.log
echo.
pause