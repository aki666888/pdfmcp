#!/usr/bin/env python3
"""
Full MCP Server for PharmaCare Form Filler
With auto-fill and PDF save functionality
"""

import asyncio
import sys
import os
import subprocess
import json
from typing import Any, Dict
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp.server import NotificationOptions, Server

# Initialize MCP server
server = Server("pharmacare-form")

# Form path
FORM_PATH = r"C:\mcp-servers\pharmacare-form"

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools for form filling"""
    return [
        Tool(
            name="fill_macs_form",
            description="Fill the PharmaCare MACS form with patient information and save as PDF",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient's full name (required)"
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
                        "enum": ["headache", "uti", "acne", "allergic_rhinitis", "dermatitis", 
                                 "fungal_infection", "herpes_labialis", "impetigo"],
                        "description": "Medical condition"
                    },
                    "symptoms": {
                        "type": "string",
                        "description": "Patient symptoms and signs"
                    },
                    "medical_history": {
                        "type": "string",
                        "description": "Relevant medical history"
                    },
                    "diagnosis": {
                        "type": "string",
                        "description": "Clinical diagnosis"
                    },
                    "medication": {
                        "type": "string",
                        "description": "Medication details (sig, mitte, refills)"
                    },
                    "save_pdf": {
                        "type": "boolean",
                        "description": "Save as PDF after filling (default: true)",
                        "default": True
                    }
                },
                "required": ["patient_name"]
            }
        ),
        Tool(
            name="quick_fill_headache",
            description="Quick fill form for headache patient with standard treatment",
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
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number (optional)"
                    }
                },
                "required": ["patient_name", "phn"]
            }
        ),
        Tool(
            name="quick_fill_uti",
            description="Quick fill form for UTI patient with standard antibiotic",
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
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number (optional)"
                    }
                },
                "required": ["patient_name", "phn"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "fill_macs_form":
        patient_name = arguments.get("patient_name", "")
        
        # Create form data
        form_data = {
            "patient_name": patient_name,
            "phn": arguments.get("phn", ""),
            "phone": arguments.get("phone", ""),
            "condition": arguments.get("condition", ""),
            "symptoms": arguments.get("symptoms", ""),
            "medical_history": arguments.get("medical_history", ""),
            "diagnosis": arguments.get("diagnosis", ""),
            "medication": arguments.get("medication", ""),
            "save_pdf": arguments.get("save_pdf", True)
        }
        
        # Launch form filler script
        try:
            # Save form data to temp file to avoid JSON parsing issues
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            json.dump(form_data, temp_file)
            temp_file.close()
            
            script = f"""
import sys
import json
sys.path.append(r'{FORM_PATH}')
from mapped_pdf_filler import fill_mapped_pdf as fill_and_save_form

# Load form data
with open(r'{temp_file.name}', 'r') as f:
    data = json.load(f)

# Fill and save form
result = fill_and_save_form(data)
print(result)
"""
            
            # Run the script
            result = subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return [TextContent(
                    type="text",
                    text=f"✅ MACS form filled for {patient_name}\n{result.stdout}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Error filling form: {result.stderr}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error: {str(e)}"
            )]
    
    elif name == "quick_fill_headache":
        # Pre-filled headache template
        patient_name = arguments.get("patient_name", "")
        phn = arguments.get("phn", "")
        phone = arguments.get("phone", "(250) 555-0000")
        
        form_data = {
            "patient_name": patient_name,
            "phn": phn,
            "phone": phone,
            "condition": "headache",
            "symptoms": "Patient presents with bilateral tension-type headache, duration 2 days. No red flags. Pain 6/10.",
            "medical_history": "No significant PMHx. No drug allergies. No contraindications.",
            "diagnosis": "Tension headache",
            "medication": "Acetaminophen 500mg PO q4-6h PRN #30 Refills: 0",
            "save_pdf": True
        }
        
        # Use the same fill logic
        return await handle_call_tool("fill_macs_form", form_data)
    
    elif name == "quick_fill_uti":
        # Pre-filled UTI template
        patient_name = arguments.get("patient_name", "")
        phn = arguments.get("phn", "")
        phone = arguments.get("phone", "(250) 555-0000")
        
        form_data = {
            "patient_name": patient_name,
            "phn": phn,
            "phone": phone,
            "condition": "uti",
            "symptoms": "Dysuria, frequency, urgency x 2 days. No fever, flank pain, or vaginal symptoms.",
            "medical_history": "No recurrent UTIs. No drug allergies.",
            "diagnosis": "Uncomplicated UTI",
            "medication": "Nitrofurantoin 100mg PO BID #10 Refills: 0",
            "save_pdf": True
        }
        
        # Use the same fill logic
        return await handle_call_tool("fill_macs_form", form_data)
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pharmacare-form",
                server_version="2.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())