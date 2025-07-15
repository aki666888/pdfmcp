#!/usr/bin/env python3
"""
MCP Server for PharmaCare Form Filler
Allows Claude Desktop to fill the MACS form
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp.server import NotificationOptions, Server

# Initialize MCP server
server = Server("pharmacare-form-filler")

# Form image path
FORM_IMAGE_PATH = r"C:\mcp-servers\pharmacare-form\blank.jpg"
FORM_FILLER_PATH = r"C:\mcp-servers\pharmacare-form\form_filler.py"

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools for form filling"""
    return [
        Tool(
            name="fill_macs_form",
            description="Fill the PharmaCare MACS form with patient information",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient's full name"
                    },
                    "phn": {
                        "type": "string",
                        "description": "Personal Health Number (10 digits)"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Patient's phone number"
                    },
                    "condition": {
                        "type": "string",
                        "description": "Medical condition (e.g., headache, acne, uti, allergic_rhinitis, dermatitis)"
                    },
                    "symptoms": {
                        "type": "string",
                        "description": "Patient symptoms and signs"
                    },
                    "diagnosis": {
                        "type": "string",
                        "description": "Clinical diagnosis"
                    },
                    "recommendations": {
                        "type": "string",
                        "description": "Treatment recommendations"
                    }
                },
                "required": ["patient_name"]
            }
        ),
        Tool(
            name="open_blank_form",
            description="Open a blank PharmaCare MACS form",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="quick_fill_headache",
            description="Quick fill form for headache patient",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient's name"
                    },
                    "phn": {
                        "type": "string",
                        "description": "Personal Health Number"
                    }
                },
                "required": ["patient_name", "phn"]
            }
        ),
        Tool(
            name="quick_fill_uti",
            description="Quick fill form for UTI patient",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient's name"
                    },
                    "phn": {
                        "type": "string",
                        "description": "Personal Health Number"
                    }
                },
                "required": ["patient_name", "phn"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "open_blank_form":
        # Open blank form
        try:
            subprocess.Popen([sys.executable, FORM_FILLER_PATH])
            return [TextContent(type="text", text="Blank MACS form opened successfully")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error opening form: {str(e)}")]
    
    elif name == "fill_macs_form":
        # Create a temporary JSON file with form data
        form_data = {
            "patient_info": {
                "name": arguments.get("patient_name", ""),
                "phn": arguments.get("phn", ""),
                "phone": arguments.get("phone", "")
            },
            "assessment": {
                "symptoms": arguments.get("symptoms", ""),
                "diagnosis": arguments.get("diagnosis", "")
            },
            "recommendations": arguments.get("recommendations", ""),
            "condition": arguments.get("condition", "")
        }
        
        # Save to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(form_data, f)
            temp_file = f.name
        
        # Launch form filler with data
        try:
            args = [
                sys.executable, 
                FORM_FILLER_PATH,
                arguments.get("patient_name", ""),
                arguments.get("condition", ""),
                arguments.get("phn", ""),
                arguments.get("phone", "")
            ]
            subprocess.Popen(args)
            
            return [TextContent(
                type="text", 
                text=f"MACS form opened with patient: {arguments.get('patient_name', 'Unknown')}\n"
                     f"Condition: {arguments.get('condition', 'Not specified')}\n"
                     f"PHN: {arguments.get('phn', 'Not provided')}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error filling form: {str(e)}")]
    
    elif name == "quick_fill_headache":
        # Quick fill for headache
        args = [
            sys.executable,
            FORM_FILLER_PATH,
            arguments.get("patient_name", ""),
            "headache",
            arguments.get("phn", ""),
            arguments.get("phone", "(250) 555-0000")
        ]
        
        try:
            subprocess.Popen(args)
            return [TextContent(
                type="text",
                text=f"MACS form opened for headache patient: {arguments.get('patient_name')}\n"
                     f"Pre-filled with standard headache assessment and acetaminophen recommendation"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "quick_fill_uti":
        # Quick fill for UTI
        args = [
            sys.executable,
            FORM_FILLER_PATH,
            arguments.get("patient_name", ""),
            "uti",
            arguments.get("phn", ""),
            arguments.get("phone", "(250) 555-0000")
        ]
        
        try:
            subprocess.Popen(args)
            return [TextContent(
                type="text",
                text=f"MACS form opened for UTI patient: {arguments.get('patient_name')}\n"
                     f"Pre-filled with standard UTI assessment"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pharmacare-form-filler",
                server_version="1.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())