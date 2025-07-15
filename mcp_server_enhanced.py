#!/usr/bin/env python3
"""
Enhanced MCP Server for PharmaCare MACS Form
Supports condition selection and highlighting
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    InitializationOptions,
    Tool,
    TextContent,
    CallToolResult
)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_pdf_filler import fill_enhanced_pdf

# Initialize the server
server = Server(name="pharmacare-form")

# Available conditions for Claude Desktop
AVAILABLE_CONDITIONS = {
    # Skin conditions
    'acne': 'Acne - inflammatory skin condition',
    'dermatitis': 'Dermatitis - skin inflammation',
    'impetigo': 'Impetigo - bacterial skin infection',
    'shingles': 'Shingles - viral infection causing painful rash',
    'urticaria': 'Urticaria/hives - including insect bites',
    
    # Fungal infections
    'tinea_pedis': "Tinea pedis - athlete's foot fungal infection",
    'tinea_corporis': 'Tinea corporis - ringworm on body',
    'tinea_cruris': 'Tinea cruris - jock itch',
    'onychomycosis': 'Onychomycosis - fungal nail infection',
    'vaginal_candidiasis': 'Vaginal candidiasis - yeast infection',
    'oropharyngeal_candidiasis': 'Oropharyngeal candidiasis - oral thrush',
    
    # Pain conditions
    'headache': 'Headache - including tension and mild migraine',
    'dysmenorrhea': 'Dysmenorrhea - painful menstruation',
    'musculoskeletal_pain': 'Musculoskeletal pain - muscle/joint pain',
    
    # Digestive
    'dyspepsia': 'Dyspepsia - indigestion',
    'gastroesophageal_reflux': 'GERD - acid reflux',
    'oral_ulcers': 'Oral ulcers - mouth sores',
    
    # Infections
    'conjunctivitis': 'Conjunctivitis - pink eye',
    'herpes_labialis': 'Herpes labialis - cold sores',
    'uti': 'UTI - urinary tract infection',
    'threadworms': 'Threadworms/pinworms - intestinal parasites',
    
    # Other
    'allergic_rhinitis': 'Allergic rhinitis - hay fever',
    'hemorrhoids': 'Hemorrhoids - swollen rectal veins',
    'nicotine_dependence': 'Nicotine dependence - smoking cessation',
    'contraception': 'Contraception - birth control'
}

@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        Tool(
            name="fill_pharmacare_form",
            description="Fill the PharmaCare MACS form with patient information. Supports multiple condition selection.",
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
                    "conditions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": f"List of condition codes to highlight. Available: {', '.join(AVAILABLE_CONDITIONS.keys())}"
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
                    }
                },
                "required": ["patient_name", "phn", "conditions"]
            }
        ),
        Tool(
            name="list_conditions",
            description="List all available conditions that can be selected on the MACS form",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="suggest_condition",
            description="Suggest appropriate condition codes based on symptoms",
            inputSchema={
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "string",
                        "description": "Patient's symptoms description"
                    }
                },
                "required": ["symptoms"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    
    if name == "fill_pharmacare_form":
        try:
            # Validate conditions
            conditions = arguments.get('conditions', [])
            validated_conditions = []
            
            for condition in conditions:
                if condition in AVAILABLE_CONDITIONS:
                    validated_conditions.append(condition)
                else:
                    # Try to find a close match
                    condition_lower = condition.lower().replace(' ', '_')
                    if condition_lower in AVAILABLE_CONDITIONS:
                        validated_conditions.append(condition_lower)
            
            # Update arguments with validated conditions
            arguments['conditions'] = validated_conditions
            
            # Fill the form
            result = fill_enhanced_pdf(arguments)
            
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
    
    elif name == "list_conditions":
        # Format conditions list
        conditions_text = "Available conditions for MACS form:\n\n"
        
        # Group by category
        categories = {
            "Skin Conditions": ['acne', 'dermatitis', 'impetigo', 'shingles', 'urticaria'],
            "Fungal Infections": ['tinea_pedis', 'tinea_corporis', 'tinea_cruris', 
                                 'onychomycosis', 'vaginal_candidiasis', 'oropharyngeal_candidiasis'],
            "Pain": ['headache', 'dysmenorrhea', 'musculoskeletal_pain'],
            "Digestive": ['dyspepsia', 'gastroesophageal_reflux', 'oral_ulcers'],
            "Infections": ['conjunctivitis', 'herpes_labialis', 'uti', 'threadworms'],
            "Other": ['allergic_rhinitis', 'hemorrhoids', 'nicotine_dependence', 'contraception']
        }
        
        for category, codes in categories.items():
            conditions_text += f"{category}:\n"
            for code in codes:
                if code in AVAILABLE_CONDITIONS:
                    conditions_text += f"  • {code}: {AVAILABLE_CONDITIONS[code]}\n"
            conditions_text += "\n"
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=conditions_text
            )]
        )
    
    elif name == "suggest_condition":
        symptoms = arguments.get('symptoms', '').lower()
        suggestions = []
        
        # Simple keyword matching
        keyword_map = {
            'feet': ['tinea_pedis'],
            'foot': ['tinea_pedis'],
            'athlete': ['tinea_pedis'],
            'headache': ['headache'],
            'migraine': ['headache'],
            'urinary': ['uti'],
            'bladder': ['uti'],
            'burning': ['uti'],
            'acne': ['acne'],
            'pimples': ['acne'],
            'cold sore': ['herpes_labialis'],
            'period': ['dysmenorrhea'],
            'menstrual': ['dysmenorrhea'],
            'cramps': ['dysmenorrhea'],
            'itchy': ['urticaria', 'tinea_pedis', 'dermatitis'],
            'rash': ['dermatitis', 'shingles', 'urticaria'],
            'fungal': ['tinea_pedis', 'tinea_corporis', 'tinea_cruris', 'vaginal_candidiasis'],
            'yeast': ['vaginal_candidiasis', 'oropharyngeal_candidiasis'],
            'pink eye': ['conjunctivitis'],
            'heartburn': ['gastroesophageal_reflux'],
            'acid reflux': ['gastroesophageal_reflux'],
            'smoking': ['nicotine_dependence'],
            'quit smoking': ['nicotine_dependence']
        }
        
        for keyword, conditions in keyword_map.items():
            if keyword in symptoms:
                suggestions.extend(conditions)
        
        # Remove duplicates
        suggestions = list(set(suggestions))
        
        if suggestions:
            result = f"Based on symptoms '{arguments['symptoms']}', suggested conditions:\n"
            for s in suggestions:
                result += f"  • {s}: {AVAILABLE_CONDITIONS[s]}\n"
        else:
            result = f"No specific conditions matched the symptoms. Please review available conditions with 'list_conditions' tool."
        
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
    print("Enhanced PharmaCare MCP Server starting...", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pharmacare-form-enhanced",
                server_version="2.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())