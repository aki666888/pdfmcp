#!/usr/bin/env python3
"""
Mapped PDF Filler
Uses the mapping created by form_field_mapper.py to fill PDFs
"""

import os
import json
import fitz  # PyMuPDF
from datetime import datetime

class MappedPDFFiller:
    def __init__(self, mapping_file="macs_form_mapping.json"):
        """Initialize with mapping file"""
        self.mapping_file = mapping_file
        self.mapping = None
        self.load_mapping()
        
    def load_mapping(self):
        """Load the field mapping"""
        mapping_path = os.path.join(os.path.dirname(__file__), self.mapping_file)
        if os.path.exists(mapping_path):
            with open(mapping_path, 'r') as f:
                self.mapping = json.load(f)
        else:
            # Default mapping if file doesn't exist
            self.mapping = {
                'pdf_file': 'blank.pdf',
                'fields': {},
                'context': 'PharmaCare MACS form'
            }
    
    def fill_pdf(self, data):
        """Fill PDF based on mapping and data from Claude Desktop"""
        try:
            # Get PDF path
            pdf_path = os.path.join(os.path.dirname(__file__), self.mapping['pdf_file'])
            if not os.path.exists(pdf_path):
                pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
            
            # Open PDF
            doc = fitz.open(pdf_path)
            
            # Process each field type
            for field_type, positions in self.mapping['fields'].items():
                # Get value for this field type
                value = self._get_field_value(field_type, data)
                
                if value:
                    # Add text at each position
                    for pos in positions:
                        page = doc[pos['page']]
                        
                        # For checkboxes, add highlighting or marking
                        if field_type.startswith('checkbox_'):
                            if value == True or value == 'checked':
                                # Option 1: Draw a circle around the checkbox
                                rect = fitz.Rect(pos['x']-5, pos['y']-5, pos['x']+15, pos['y']+15)
                                page.draw_circle(fitz.Point(pos['x']+5, pos['y']+5), 8)
                                page.finish(color=(1, 0, 0), width=2)
                                
                                # Option 2: Or highlight the text next to checkbox
                                # highlight_rect = fitz.Rect(pos['x']+20, pos['y']-2, pos['x']+150, pos['y']+18)
                                # page.add_highlight_annot(highlight_rect)
                        else:
                            # For text fields
                            page.insert_text(
                                (pos['x'] + 5, pos['y'] + 15),
                                str(value),
                                fontsize=10,
                                color=(0, 0, 0)
                            )
            
            # Create output directory
            patient_name = data.get("patient_name", "Unknown")
            patient_folder = patient_name.split(',')[0].strip() if ',' in patient_name else patient_name.split()[0]
            patient_folder = "".join(c for c in patient_folder if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            save_dir = f"C:/forms/{patient_folder}"
            os.makedirs(save_dir, exist_ok=True)
            
            # Save PDF
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.pdf")
            doc.save(output_path)
            doc.close()
            
            # Save JSON data
            json_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.json")
            with open(json_path, 'w') as f:
                json.dump({
                    "form_data": data,
                    "timestamp": timestamp,
                    "pdf_path": output_path
                }, f, indent=2)
            
            return {
                "success": True,
                "pdf_path": output_path,
                "json_path": json_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_field_value(self, field_type, data):
        """Get value for a specific field type from data"""
        # Direct field mappings
        direct_mappings = {
            'patient_name': data.get('patient_name', ''),
            'phn': data.get('phn', ''),
            'phone': data.get('phone', ''),
            'symptoms': data.get('symptoms', ''),
            'medical_history': data.get('medical_history', ''),
            'diagnosis': data.get('diagnosis', ''),
            'medication': data.get('medication', ''),
            'date': datetime.now().strftime("%Y-%m-%d"),
        }
        
        if field_type in direct_mappings:
            return direct_mappings[field_type]
        
        # Checkbox mappings
        if field_type.startswith('checkbox_'):
            checkbox_type = field_type.replace('checkbox_', '')
            
            # Pre-checked items
            if checkbox_type in ['pharmacist', 'eligible', 'consent']:
                return True
                
            # Condition checkboxes
            if checkbox_type == data.get('condition', '').lower():
                return True
                
            # Prescription checkbox
            if checkbox_type == 'prescription' and data.get('prescription_issued', False):
                return True
                
        return None

# Quick function for MCP
def fill_mapped_pdf(data):
    """Fill PDF using mapping"""
    filler = MappedPDFFiller()
    result = filler.fill_pdf(data)
    
    if result["success"]:
        return f"Form saved successfully!\nPDF: {result['pdf_path']}\nData: {result['json_path']}"
    else:
        return f"Error: {result['error']}"

if __name__ == "__main__":
    # Test
    test_data = {
        "patient_name": "Test Patient",
        "phn": "1234567890",
        "phone": "(250) 555-0123",
        "condition": "headache",
        "symptoms": "Test symptoms",
        "medical_history": "No allergies",
        "diagnosis": "Test diagnosis",
        "medication": "Test medication",
        "prescription_issued": True
    }
    
    result = fill_mapped_pdf(test_data)
    print(result)