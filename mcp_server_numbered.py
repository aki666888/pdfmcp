#!/usr/bin/env python3
"""
MCP Server with Numbered Condition Box Support
Claude Desktop can specify condition numbers instead of names
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult
)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_pdf_filler_v2 import fill_pdf_with_numbers

# Initialize the server
server = Server(name="pharmacare-form")

@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        Tool(
            name="fill_pharmacare_form",
            description="Fill the PharmaCare MACS form with numbered condition selection",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient's full name"
                    },
                    "phn": {
                        "type": "string",
                        "description": "Personal Health Number"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Patient phone number"
                    },
                    "condition_numbers": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of condition box numbers to highlight (e.g., [1, 3, 5])"
                    },
                    "symptoms": {
                        "type": "string",
                        "description": "Patient's symptoms"
                    },
                    "medical_history": {
                        "type": "string",
                        "description": "Relevant medical history"
                    },
                    "diagnosis": {
                        "type": "string",
                        "description": "Diagnosis"
                    },
                    "medication": {
                        "type": "string",
                        "description": "Prescribed medication"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date (YYYY-MM-DD format)"
                    }
                },
                "required": ["patient_name", "phn"]
            }
        ),
        Tool(
            name="list_condition_boxes",
            description="List the numbered condition boxes and their typical conditions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="quick_fill_with_conditions",
            description="Quick fill with common condition combinations",
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
                    "condition_preset": {
                        "type": "string",
                        "enum": ["skin", "infection", "pain", "respiratory"],
                        "description": "Preset condition group"
                    }
                },
                "required": ["patient_name", "phn", "condition_preset"]
            }
        )
    ]

# Condition box mappings based on actual form layout
CONDITION_BOX_MAP = {
    1: "Contraception",
    2: "Acne", 
    3: "Allergic rhinitis",
    4: "Conjunctivitis",
    # 5 removed - was Dermatitis header
    6: "allergic/contact",
    7: "atopic",
    8: "diaper rash",
    9: "seborrheic",
    10: "Dysmenorrhea",
    11: "Dyspepsia",
    12: "Fungal infections",
    13: "Onychomycosis",
    14: "Tinea corporis infection",
    15: "Tinea cruris infection",
    16: "Tinea pedis infection",
    17: "Gastroesophageal reflux disease",
    18: "Headache",
    19: "Nicotine dependence",
    20: "Hemorrhoids",
    21: "Herpes labialis",
    22: "Impetigo",
    23: "Oral ulcers",
    24: "Oropharyngeal candidiasis",
    25: "Musculoskeletal pain",
    26: "Shingles",
    27: "Threadworms or pinworms",
    28: "Urinary tract infection",
    29: "Urticaria, including insect bites",
    30: "Vaginal candidiasis"
}

# Preset condition groups (updated to match actual box numbers)
CONDITION_PRESETS = {
    "skin": [2, 6, 7, 22, 26, 29],  # Acne, allergic/contact, atopic, Impetigo, Shingles, Urticaria
    "infection": [28, 30, 16, 14, 15],  # UTI, Vaginal candidiasis, Tinea infections
    "pain": [18, 10, 25],  # Headache, Dysmenorrhea, Musculoskeletal pain
    "respiratory": [3, 4, 21]  # Allergic rhinitis, Conjunctivitis, Herpes labialis
}

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    
    if name == "fill_pharmacare_form":
        try:
            # Fill the form with numbered conditions
            result = fill_pdf_with_numbers(arguments)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=result
                )]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error filling form: {str(e)}"
                )]
            )
    
    elif name == "list_condition_boxes":
        # Format condition box list
        text = "Numbered Condition Boxes on MACS Form:\n\n"
        
        for num, condition in CONDITION_BOX_MAP.items():
            text += f"Box #{num}: {condition}\n"
        
        text += "\nTo select conditions, provide the box numbers in the condition_numbers array."
        text += "\nExample: [2, 5, 9] would select Acne, Dermatitis, and Headache."
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=text
            )]
        )
    
    elif name == "quick_fill_with_conditions":
        preset = arguments.get('condition_preset')
        condition_numbers = CONDITION_PRESETS.get(preset, [])
        
        # Create full form data
        form_data = {
            "patient_name": arguments['patient_name'],
            "phn": arguments['phn'],
            "phone": arguments.get('phone', ''),
            "condition_numbers": condition_numbers,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Add preset-specific defaults
        if preset == "skin":
            form_data.update({
                "symptoms": "Skin irritation, rash, or lesions",
                "diagnosis": "Dermatological condition",
                "medication": "Topical treatment as appropriate"
            })
        elif preset == "infection":
            form_data.update({
                "symptoms": "Signs of infection",
                "diagnosis": "Bacterial/fungal infection",
                "medication": "Antimicrobial therapy"
            })
        elif preset == "pain":
            form_data.update({
                "symptoms": "Pain symptoms",
                "diagnosis": "Pain management required",
                "medication": "Analgesics as appropriate"
            })
        elif preset == "respiratory":
            form_data.update({
                "symptoms": "Respiratory/allergic symptoms",
                "diagnosis": "Upper respiratory condition",
                "medication": "Symptomatic treatment"
            })
        
        result = fill_pdf_with_numbers(form_data)
        
        selected_conditions = [CONDITION_BOX_MAP.get(n, f"Box {n}") for n in condition_numbers]
        result += f"\n\nSelected conditions: {', '.join(selected_conditions)}"
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=result
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
    # Print to stderr for debugging
    print("PharmaCare MCP Server (Numbered Conditions) starting...", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pharmacare-form-numbered",
                server_version="3.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())