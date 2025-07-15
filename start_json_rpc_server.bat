@echo off
echo Starting JSON-RPC Server for PharmaCare Forms...
echo Server will run on: http://localhost:8080
echo.
echo Use with OpenRPC MCP in Claude Desktop:
echo 1. Call method: fillPharmaCareForm
echo 2. Server URL: http://localhost:8080
echo.
"C:\Program Files\Python312\python.exe" json_rpc_server.py
pause