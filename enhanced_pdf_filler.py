#!/usr/bin/env python3
"""
Enhanced PDF Filler with Text Search and Highlighting
Allows Claude Desktop to specify conditions and the system will find and highlight them
"""

import os
import json
import fitz  # PyMuPDF
from datetime import datetime
import re

class EnhancedPDFFiller:
    def __init__(self, mapping_file="macs_form_mapping.json"):
        """Initialize with mapping file"""
        self.mapping_file = mapping_file
        self.mapping = None
        self.load_mapping()
        
        # Condition text mapping - exact text as it appears on the PDF
        self.condition_map = {
            # First column
            'contraception': 'Contraception',
            'acne': 'Acne',
            'allergic_rhinitis': 'Allergic rhinitis',
            'conjunctivitis': 'Conjunctivitis',
            'dermatitis': 'Dermatitis',
            'dermatitis_allergic': 'allergic/contact',
            'dermatitis_atopic': 'atopic',
            'dermatitis_diaper': 'diaper rash',
            'dermatitis_seborrheic': 'seborrheic',
            
            # Second column
            'dysmenorrhea': 'Dysmenorrhea',
            'dyspepsia': 'Dyspepsia',
            'fungal_infections': 'Fungal infections',
            'onychomycosis': 'Onychomycosis',
            'tinea_corporis': 'Tinea corporis infection',
            'tinea_cruris': 'Tinea cruris infection',
            'tinea_pedis': 'Tinea pedis infection',
            'gastroesophageal_reflux': 'Gastroesophageal reflux disease',
            
            # Third column
            'headache': 'Headache',
            'hemorrhoids': 'Hemorrhoids',
            'herpes_labialis': 'Herpes labialis',
            'impetigo': 'Impetigo',
            'oral_ulcers': 'Oral ulcers',
            'oropharyngeal_candidiasis': 'Oropharyngeal candidiasis',
            'musculoskeletal_pain': 'Musculoskeletal pain',
            'shingles': 'Shingles',
            
            # Fourth column
            'nicotine_dependence': 'Nicotine dependence',
            'threadworms': 'Threadworms or pinworms',
            'uti': 'Urinary tract infection',
            'urticaria': 'Urticaria, including insect bites',
            'vaginal_candidiasis': 'Vaginal candidiasis'
        }
        
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
    
    def find_and_highlight_condition(self, page, condition_code):
        """Find and highlight a condition on the page"""
        # Get the exact text for this condition
        condition_text = self.condition_map.get(condition_code)
        if not condition_text:
            print(f"Unknown condition code: {condition_code}")
            return False
            
        # Search for the text on the page
        text_instances = page.search_for(condition_text)
        
        if text_instances:
            for inst in text_instances:
                # Method 1: Highlight the text with yellow background
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0))  # Yellow
                highlight.update()
                
                # Method 2: Draw a red circle/checkbox next to the text
                # Find the checkbox position (usually to the left of the text)
                checkbox_x = inst.x0 - 20  # 20 pixels to the left
                checkbox_y = inst.y0 + (inst.y1 - inst.y0) / 2  # Middle of text height
                
                # Draw a filled circle to indicate selection
                page.draw_circle(
                    center=fitz.Point(checkbox_x, checkbox_y),
                    radius=5,
                    color=(1, 0, 0),  # Red
                    fill=(1, 0, 0)
                )
                
                # Alternative: Draw a checkmark
                # page.draw_line(
                #     fitz.Point(checkbox_x - 3, checkbox_y),
                #     fitz.Point(checkbox_x, checkbox_y + 3),
                #     color=(1, 0, 0),
                #     width=2
                # )
                # page.draw_line(
                #     fitz.Point(checkbox_x, checkbox_y + 3),
                #     fitz.Point(checkbox_x + 5, checkbox_y - 5),
                #     color=(1, 0, 0),
                #     width=2
                # )
                
            return True
        else:
            print(f"Could not find text '{condition_text}' on page")
            return False
    
    def fill_pdf(self, data):
        """Fill PDF with enhanced condition selection"""
        try:
            # Get PDF path
            pdf_path = os.path.join(os.path.dirname(__file__), self.mapping['pdf_file'])
            if not os.path.exists(pdf_path):
                pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
            
            # Open PDF
            doc = fitz.open(pdf_path)
            
            # First, handle conditions if specified
            conditions = data.get('conditions', [])
            if isinstance(conditions, str):
                conditions = [conditions]
            
            # Search and highlight each condition
            for condition in conditions:
                # Normalize condition name
                condition_normalized = condition.lower().replace(' ', '_').replace("'", '')
                
                # Try to find on each page (usually page 0 for MACS form)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    self.find_and_highlight_condition(page, condition_normalized)
            
            # Process mapped fields
            for field_type, positions in self.mapping['fields'].items():
                # Get value for this field type
                value = self._get_field_value(field_type, data)
                
                if value and field_type not in ['checkbox_contraception', 'checkbox_acne', 'checkbox_headache', 
                                                 'checkbox_uti', 'checkbox_tinea_pedis']:  # Skip individual condition checkboxes
                    # Add text at each position
                    for pos in positions:
                        page = doc[pos['page']]
                        
                        # For pre-checked items
                        if field_type in ['checkbox_pharmacist', 'checkbox_eligible', 'checkbox_consent']:
                            # Draw a filled circle
                            page.draw_circle(
                                center=fitz.Point(pos['x'] + 5, pos['y'] + 5),
                                radius=5,
                                color=(0, 0, 0),
                                fill=(0, 0, 0)
                            )
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
                    "pdf_path": output_path,
                    "conditions_selected": conditions
                }, f, indent=2)
            
            return {
                "success": True,
                "pdf_path": output_path,
                "json_path": json_path,
                "conditions_highlighted": conditions
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
        
        # Pre-checked items
        if field_type in ['checkbox_pharmacist', 'checkbox_eligible', 'checkbox_consent']:
            return True
            
        return None

# Quick function for MCP
def fill_enhanced_pdf(data):
    """Fill PDF with enhanced condition selection"""
    filler = EnhancedPDFFiller()
    result = filler.fill_pdf(data)
    
    if result["success"]:
        conditions_text = ", ".join(result.get("conditions_highlighted", []))
        return f"Form saved successfully!\nPDF: {result['pdf_path']}\nData: {result['json_path']}\nConditions highlighted: {conditions_text}"
    else:
        return f"Error: {result['error']}"

if __name__ == "__main__":
    # Test with multiple conditions
    test_data = {
        "patient_name": "John Doe",
        "phn": "9876543210",
        "phone": "(250) 555-1234",
        "conditions": ["tinea_pedis", "headache"],  # Claude Desktop can specify multiple
        "symptoms": "Itchy feet, frequent headaches",
        "medical_history": "No known allergies",
        "diagnosis": "Athlete's foot and tension headaches",
        "medication": "Topical antifungal, acetaminophen",
        "prescription_issued": True
    }
    
    result = fill_enhanced_pdf(test_data)
    print(result)