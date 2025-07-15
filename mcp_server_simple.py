#!/usr/bin/env python3
"""
Simple MCP Server for PharmaCare Form Filler
Minimal version for testing
"""

import asyncio
import sys
import os
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp.server import NotificationOptions, Server

# Initialize MCP server
server = Server("pharmacare-form")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="test_pharmacare",
            description="Test if PharmaCare MCP server is working",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="open_form",
            description="Open the PharmaCare MACS form",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient's name (optional)"
                    }
                },
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "test_pharmacare":
        return [TextContent(
            type="text", 
            text="✅ PharmaCare MCP server is working! You can now use the form filling tools."
        )]
    
    elif name == "open_form":
        patient = arguments.get("patient_name", "New Patient")
        
        # Try to launch the simple form
        try:
            import subprocess
            form_path = os.path.join(os.path.dirname(__file__), "simple_form.py")
            
            if os.path.exists(form_path):
                subprocess.Popen([sys.executable, form_path])
                return [TextContent(
                    type="text",
                    text=f"✅ PharmaCare MACS form opened for patient: {patient}\n"
                         f"The form window should appear on your screen."
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Form file not found at: {form_path}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error opening form: {str(e)}"
            )]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pharmacare-form",
                server_version="1.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())