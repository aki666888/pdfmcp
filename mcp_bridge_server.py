#!/usr/bin/env python3
"""
MCP Bridge Server - Connects Claude Desktop to existing PDF filler
Takes JSON input and calls the existing enhanced_pdf_filler_v2
"""

import asyncio
import sys
import os
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, CallToolResult

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your existing PDF filler
from enhanced_pdf_filler_v2 import fill_pdf_with_numbers

# Initialize the server
server = Server(name="pharmacare-bridge")

@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        Tool(
            name="fill_form",
            description="Fill PharmaCare form with provided JSON data",
            inputSchema={
                "type": "object",
                "properties": {
                    "form_data": {
                        "type": "object",
                        "description": "Complete form data object",
                        "properties": {
                            "patient_name": {"type": "string"},
                            "phn": {"type": "string"},
                            "phone": {"type": "string"},
                            "condition_numbers": {
                                "type": "array",
                                "items": {"type": "integer"}
                            },
                            "symptoms": {"type": "string"},
                            "medical_history": {"type": "string"},
                            "diagnosis": {"type": "string"},
                            "medication": {"type": "string"}
                        }
                    }
                },
                "required": ["form_data"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    
    if name == "fill_form":
        try:
            # Extract the form data
            form_data = arguments.get('form_data', {})
            
            # Log what we received
            print(f"Received form data: {json.dumps(form_data, indent=2)}", file=sys.stderr)
            
            # Call your existing PDF filler
            result = fill_pdf_with_numbers(form_data)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=result
                )]
            )
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg, file=sys.stderr)
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=error_msg
                )]
            )
    
    else:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
        )

async def main():
    """Main entry point"""
    print("PharmaCare Bridge Server starting...", file=sys.stderr)
    print("This server connects Claude Desktop to your existing PDF filler", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pharmacare-bridge",
                server_version="1.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())