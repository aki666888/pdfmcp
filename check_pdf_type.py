#!/usr/bin/env python3
"""
Check PDF type and structure
"""

import os
from PyPDF2 import PdfReader
import fitz

def check_pdf_type():
    """Check what type of PDF this is"""
    pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF not found at: {pdf_path}")
        return
    
    print("=== Checking PDF Type ===\n")
    
    # Check with PyPDF2
    try:
        reader = PdfReader(pdf_path)
        
        # Check for XFA forms
        if '/AcroForm' in reader.trailer['/Root']:
            acroform = reader.trailer['/Root']['/AcroForm']
            if '/XFA' in acroform:
                print("This is an XFA (XML Forms Architecture) PDF")
            else:
                print("This is an AcroForm PDF")
                
            # Try to get fields differently
            if hasattr(reader, 'get_form_text_fields'):
                fields = reader.get_form_text_fields()
                print(f"Text fields found: {len(fields)}")
                for name, value in fields.items():
                    print(f"  {name}: {value}")
        else:
            print("No AcroForm found in PDF")
            
    except Exception as e:
        print(f"PyPDF2 error: {e}")
    
    print("\n=== Checking with PyMuPDF ===\n")
    
    # Check with PyMuPDF
    try:
        doc = fitz.open(pdf_path)
        
        # Check if it's a form
        is_form = doc.is_form_pdf
        print(f"Is form PDF: {is_form}")
        
        # Get metadata
        metadata = doc.metadata
        print(f"PDF Producer: {metadata.get('producer', 'Unknown')}")
        print(f"PDF Creator: {metadata.get('creator', 'Unknown')}")
        
        # Check for JavaScript (common in forms)
        js_count = doc._count_names("JavaScript")
        print(f"JavaScript entries: {js_count}")
        
        doc.close()
        
    except Exception as e:
        print(f"PyMuPDF error: {e}")
    
    print("\n=== Recommendation ===")
    print("If this PDF is not showing form fields, it might be:")
    print("1. A static PDF (not fillable)")
    print("2. An XFA form (needs special handling)")
    print("3. A PDF with JavaScript-based forms")
    print("\nYou might need to:")
    print("- Convert it to a fillable PDF using Adobe Acrobat")
    print("- Use a different PDF that has proper form fields")
    print("- Or we can overlay text on the static PDF instead")

if __name__ == "__main__":
    check_pdf_type()