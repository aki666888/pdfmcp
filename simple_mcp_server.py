#!/usr/bin/env python3
"""
Simple MCP server for PharmaCare forms - Based on official SDK
"""

import asyncio
import json
import sys
from mcp.server.fastmcp import FastMCP

# Import your existing PDF filler
try:
    from enhanced_pdf_filler_v2 import fill_pdf_with_numbers
except ImportError:
    def fill_pdf_with_numbers(data):
        return f"Error: Could not import PDF filler. Data received: {json.dumps(data, indent=2)}"

# Create the MCP server
mcp = FastMCP("PharmaCare Form Filler")

@mcp.tool()
def fill_pharmacare_form(
    patient_name: str,
    phn: str,
    phone: str,
    condition_numbers: list,
    symptoms: str,
    medical_history: str,
    diagnosis: str,
    medication: str
) -> str:
    """Fill PharmaCare MACS form with patient information."""
    
    # Create the data dictionary
    form_data = {
        "patient_name": patient_name,
        "phn": phn,
        "phone": phone,
        "condition_numbers": condition_numbers,
        "symptoms": symptoms,
        "medical_history": medical_history,
        "diagnosis": diagnosis,
        "medication": medication
    }
    
    try:
        # Call your existing PDF filler
        result = fill_pdf_with_numbers(form_data)
        return result
    except Exception as e:
        return f"Error filling form: {str(e)}"

@mcp.tool()
def list_conditions() -> str:
    """List all available condition box numbers."""
    conditions = """
Box 1: Contraception
Box 2: Acne
Box 3: Allergic rhinitis
Box 4: Conjunctivitis
Box 6: Dermatitis - allergic/contact
Box 7: Dermatitis - atopic
Box 8: Dermatitis - diaper rash
Box 9: Dermatitis - seborrheic
Box 10: Dysmenorrhea
Box 11: Dyspepsia
Box 12: Fungal infections
Box 13: Onychomycosis
Box 14: Tinea corporis infection
Box 15: Tinea cruris infection
Box 16: Tinea pedis infection
Box 17: Gastroesophageal reflux disease
Box 18: Headache
Box 19: Nicotine dependence
Box 20: Hemorrhoids
Box 21: Herpes labialis
Box 22: Impetigo
Box 23: Oral ulcers
Box 24: Oropharyngeal candidiasis
Box 25: Musculoskeletal pain
Box 26: Shingles
Box 27: Threadworms or pinworms
Box 28: Urinary tract infection
Box 29: Urticaria, including insect bites
Box 30: Vaginal candidiasis
"""
    return conditions

if __name__ == "__main__":
    print("Starting PharmaCare MCP Server...", file=sys.stderr)
    mcp.run()