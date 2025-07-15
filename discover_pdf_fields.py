#!/usr/bin/env python3
"""
Discover all fields in the fillable PDF
"""

import os
from PyPDF2 import PdfReader

def discover_pdf_fields():
    """Discover and list all fields in the PDF"""
    pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF not found at: {pdf_path}")
        return
    
    try:
        reader = PdfReader(pdf_path)
        
        # Get form fields
        if '/AcroForm' in reader.trailer['/Root']:
            print(f"PDF has {len(reader.get_fields())} form fields:\n")
            
            fields = reader.get_fields()
            
            # List all fields with their properties
            for field_name, field_obj in fields.items():
                field_type = field_obj.get('/FT', 'Unknown')
                field_value = field_obj.get('/V', '')
                field_default = field_obj.get('/DV', '')
                
                print(f"Field Name: {field_name}")
                print(f"  Type: {field_type}")
                print(f"  Current Value: {field_value}")
                print(f"  Default Value: {field_default}")
                
                # For checkboxes, show options
                if field_type == '/Btn':
                    options = field_obj.get('/Opt', [])
                    if options:
                        print(f"  Options: {options}")
                
                # Show additional properties
                if '/T' in field_obj:
                    print(f"  Display Name: {field_obj['/T']}")
                
                print("-" * 50)
        else:
            print("No form fields found in this PDF")
            
        # Also check for annotations (another way forms can be implemented)
        print("\nChecking for annotations on each page:")
        for i, page in enumerate(reader.pages):
            if '/Annots' in page:
                print(f"\nPage {i+1} has {len(page['/Annots'])} annotations")
                
    except Exception as e:
        print(f"Error reading PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    discover_pdf_fields()