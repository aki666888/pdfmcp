#!/usr/bin/env python3
"""
Analyze PDF structure using PyMuPDF
"""

import fitz  # PyMuPDF
import os

def analyze_pdf():
    """Analyze PDF structure and find form elements"""
    pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF not found at: {pdf_path}")
        return
    
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        
        print(f"PDF has {len(doc)} pages\n")
        
        # Check each page
        for page_num, page in enumerate(doc):
            print(f"\n=== Page {page_num + 1} ===")
            
            # Get widgets (form fields)
            widgets = page.widgets()
            widget_count = 0
            
            for widget in widgets:
                widget_count += 1
                print(f"\nWidget {widget_count}:")
                print(f"  Field Name: {widget.field_name}")
                print(f"  Field Type: {widget.field_type}")
                print(f"  Field Type String: {widget.field_type_string}")
                print(f"  Field Value: {widget.field_value}")
                print(f"  Field Display: {widget.field_display}")
                print(f"  Rectangle: {widget.rect}")
                
                # For checkboxes/radio buttons
                if widget.field_type in [2, 3]:  # Checkbox or Radio
                    print(f"  Is Checked: {widget.field_value}")
                
                # For text fields
                if widget.field_type == 7:  # Text
                    print(f"  Text Content: {widget.field_value}")
                    
            if widget_count == 0:
                print("  No form widgets found on this page")
                
            # Also check for annotations
            annots = page.annots()
            annot_count = 0
            
            for annot in annots:
                annot_count += 1
                print(f"\nAnnotation {annot_count}:")
                print(f"  Type: {annot.type}")
                print(f"  Content: {annot.info.get('content', 'N/A')}")
                print(f"  Rectangle: {annot.rect}")
                
        doc.close()
        
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_pdf()