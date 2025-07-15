#!/usr/bin/env python3
"""
Bridge runner - Called by the Node.js MCP server
Reads JSON from file and calls the PDF filler
"""

import sys
import json
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_pdf_filler_v2 import fill_pdf_with_numbers

def main():
    if len(sys.argv) < 2:
        print("Error: No input file provided")
        sys.exit(1)
    
    # Read the JSON file
    json_file = sys.argv[1]
    
    try:
        with open(json_file, 'r') as f:
            form_data = json.load(f)
        
        # Call the PDF filler
        result = fill_pdf_with_numbers(form_data)
        
        # Print result to stdout
        print(result)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()