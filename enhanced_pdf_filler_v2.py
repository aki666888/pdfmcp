#!/usr/bin/env python3
"""
Enhanced PDF Filler V2 - Works with numbered condition boxes
Claude Desktop can specify condition numbers instead of names
"""

import os
import json
import fitz  # PyMuPDF
from datetime import datetime
import sys

class EnhancedPDFFillerV2:
    def __init__(self, mapping_file=None):
        """Initialize with mapping file"""
        # Check multiple locations for the mapping file
        if mapping_file:
            self.mapping_file = mapping_file
        else:
            # Try different locations in order of preference
            possible_paths = [
                r"C:\forms\macs_form_mapping_v3_updated.json",
                r"C:\forms\macs_form_mapping_v3.json",
                os.path.join(os.path.dirname(__file__), "macs_form_mapping_v3.json")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.mapping_file = path
                    break
            else:
                self.mapping_file = possible_paths[0]  # Default to first option
        
        self.mapping = None
        self.load_mapping()
        
    def load_mapping(self):
        """Load the field mapping"""
        if os.path.exists(self.mapping_file):
            with open(self.mapping_file, 'r') as f:
                self.mapping = json.load(f)
                print(f"Loaded mapping from: {self.mapping_file}", file=sys.stderr)
        else:
            # Default mapping if file doesn't exist
            print(f"Mapping file not found at: {self.mapping_file}, using defaults", file=sys.stderr)
            self.mapping = {
                'pdf_file': 'blank.pdf',
                'fields': {},
                'condition_boxes': [],
                'font_size': 10,
                'context': 'PharmaCare MACS form'
            }
    
    def highlight_condition_box(self, page, box_number):
        """Highlight a condition box by number"""
        # Find the condition box
        for cond_box in self.mapping.get('condition_boxes', []):
            if cond_box['number'] == box_number and cond_box['page'] == page.number:
                x1, y1 = cond_box['x1'], cond_box['y1']
                x2, y2 = cond_box['x2'], cond_box['y2']
                
                # Method 1: Draw a yellow filled rectangle
                rect = fitz.Rect(x1, y1, x2, y2)
                # Note: PyMuPDF doesn't support opacity in draw_rect, so we use annotation instead
                highlight = page.add_highlight_annot(rect)
                highlight.set_colors(stroke=(1, 1, 0))  # Yellow
                highlight.update()
                
                # Method 2: Draw a thicker red border
                page.draw_rect(rect, color=(1, 0, 0), width=3)
                
                # Method 3: Add a checkmark or indicator
                # Draw a large checkmark
                check_x = x1 + (x2 - x1) * 0.2
                check_y = y1 + (y2 - y1) * 0.5
                
                # First stroke of checkmark
                page.draw_line(
                    fitz.Point(check_x, check_y),
                    fitz.Point(check_x + 15, check_y + 15),
                    color=(1, 0, 0),
                    width=3
                )
                
                # Second stroke of checkmark
                page.draw_line(
                    fitz.Point(check_x + 15, check_y + 15),
                    fitz.Point(check_x + 35, check_y - 20),
                    color=(1, 0, 0),
                    width=3
                )
                
                return True
        return False
    
    def fill_pdf(self, data):
        """Fill PDF with field data and highlighted conditions"""
        try:
            # Debug: Log received data
            print(f"DEBUG: Received data for {data.get('patient_name', 'Unknown')}", file=sys.stderr)
            print(f"DEBUG: Symptoms length: {len(data.get('symptoms', ''))}", file=sys.stderr)
            print(f"DEBUG: Medication length: {len(data.get('medication', ''))}", file=sys.stderr)
            # Get PDF path
            pdf_path = os.path.join(os.path.dirname(__file__), self.mapping['pdf_file'])
            if not os.path.exists(pdf_path):
                pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
            
            # Open PDF
            doc = fitz.open(pdf_path)
            
            # Handle condition numbers
            condition_numbers = data.get('condition_numbers', [])
            if isinstance(condition_numbers, int):
                condition_numbers = [condition_numbers]
            elif isinstance(condition_numbers, str):
                # Parse string like "1,3,5" or "1 3 5"
                condition_numbers = [int(x.strip()) for x in condition_numbers.replace(',', ' ').split() if x.strip().isdigit()]
            
            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Highlight condition boxes
                for box_num in condition_numbers:
                    self.highlight_condition_box(page, box_num)
                
                # Fill field boxes
                for field_type, boxes in self.mapping.get('fields', {}).items():
                    # Get value for this field
                    value = self._get_field_value(field_type, data)
                    
                    if value:
                        for box in boxes:
                            if box['page'] == page_num:
                                # Special handling for multi-line fields
                                if field_type == 'Patient Symptoms and Signs':
                                    # Symptoms field - use moderate font size
                                    rect = fitz.Rect(box['x1'] + 2, box['y1'] + 2, box['x2'] - 2, box['y2'] - 2)
                                    # Try insert_textbox first
                                    try:
                                        page.insert_textbox(
                                            rect,
                                            str(value),
                                            fontsize=9,  # Slightly larger font for symptoms
                                            color=(0, 0, 0),
                                            align=0  # Left align
                                        )
                                    except:
                                        # Fallback: manually wrap text
                                        lines = self._wrap_text(str(value), box['x2'] - box['x1'] - 10, 9)
                                        y_start = box['y1'] + 8
                                        line_height = 11
                                        
                                        for i, line in enumerate(lines):
                                            if y_start + (i * line_height) < box['y2'] - 5:
                                                page.insert_text(
                                                    (box['x1'] + 5, y_start + (i * line_height)),
                                                    line,
                                                    fontsize=9,
                                                    color=(0, 0, 0)
                                                )
                                elif field_type == 'medication':
                                    # Medication field - use smaller font for more text
                                    rect = fitz.Rect(box['x1'] + 2, box['y1'] + 2, box['x2'] - 2, box['y2'] - 2)
                                    # Try insert_textbox first
                                    try:
                                        page.insert_textbox(
                                            rect,
                                            str(value),
                                            fontsize=8,  # Smaller font for medication details
                                            color=(0, 0, 0),
                                            align=0  # Left align
                                        )
                                    except:
                                        # Fallback: manually wrap text
                                        lines = self._wrap_text(str(value), box['x2'] - box['x1'] - 10, 8)
                                        y_start = box['y1'] + 8
                                        line_height = 10
                                        
                                        for i, line in enumerate(lines):
                                            if y_start + (i * line_height) < box['y2'] - 5:
                                                page.insert_text(
                                                    (box['x1'] + 5, y_start + (i * line_height)),
                                                    line,
                                                    fontsize=8,
                                                    color=(0, 0, 0)
                                                )
                                else:
                                    # Single line text for other fields
                                    x = box['x1'] + 5
                                    y = box['y1'] + (box['y2'] - box['y1']) / 2 + 5
                                    
                                    # Insert text
                                    page.insert_text(
                                        (x, y),
                                        str(value),
                                        fontsize=self.mapping.get('font_size', 10),
                                        color=(0, 0, 0)
                                    )
            
            # Create simple filename: name_date.pdf
            patient_name = data.get("patient_name", "Unknown")
            # Get first name from "Last, First" or "First Last" format
            if ',' in patient_name:
                first_name = patient_name.split(',')[-1].strip()
            else:
                first_name = patient_name.split()[0] if patient_name.split() else "Unknown"
            
            # Clean filename
            first_name = "".join(c for c in first_name if c.isalnum() or c in ('-', '_')).strip()
            
            # Create C:/forms directory if it doesn't exist
            save_dir = "C:/forms"
            os.makedirs(save_dir, exist_ok=True)
            
            # Save PDF with simple name_date format - add timestamp to avoid overwrites
            date_str = datetime.now().strftime("%Y%m%d")
            time_str = datetime.now().strftime("%H%M%S")
            output_path = os.path.join(save_dir, f"{first_name}_{date_str}_{time_str}.pdf")
            doc.save(output_path)
            doc.close()
            
            return {
                "success": True,
                "pdf_path": output_path,
                "conditions_highlighted": condition_numbers
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _wrap_text(self, text, max_width, font_size):
        """Simple text wrapping function"""
        words = text.split()
        lines = []
        current_line = []
        
        # Approximate character width (adjust as needed)
        char_width = font_size * 0.5
        max_chars = int(max_width / char_width)
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_chars:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, split it
                    lines.append(word[:max_chars])
                    current_line = [word[max_chars:]]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _get_field_value(self, field_type, data):
        """Get value for a specific field type from data"""
        # Map field names from the PDF to our data keys
        field_mappings = {
            'patient_name': 'patient_name',
            'phn': 'phn',
            'phone': 'phone',
            'Patient Symptoms and Signs': 'symptoms',  # Map PDF field name to our data key
            'medical_history': 'medical_history',
            'diagnosis': 'diagnosis',
            'medication': 'medication',
            'date': 'date'
        }
        
        # Get the data key for this field type
        data_key = field_mappings.get(field_type, field_type)
        
        # Get the value from data
        if data_key == 'date' and data_key not in data:
            return datetime.now().strftime("%Y-%m-%d")
        
        return data.get(data_key, '')

# Quick function for MCP
def fill_pdf_with_numbers(data):
    """Fill PDF using numbered condition boxes"""
    filler = EnhancedPDFFillerV2()
    result = filler.fill_pdf(data)
    
    if result["success"]:
        conditions = result.get("conditions_highlighted", [])
        conditions_text = f"Conditions {', '.join(map(str, conditions))}" if conditions else "No conditions"
        return f"Form saved successfully!\nPDF: {result['pdf_path']}\n{conditions_text} highlighted"
    else:
        return f"Error: {result['error']}"

if __name__ == "__main__":
    # Test with condition numbers
    test_data = {
        "patient_name": "John Doe",
        "phn": "9876543210",
        "phone": "(250) 555-1234",
        "condition_numbers": [2, 5, 8],  # Claude Desktop specifies box numbers
        "symptoms": "Various symptoms",
        "medical_history": "No known allergies",
        "diagnosis": "Multiple conditions",
        "medication": "As prescribed",
        "date": "2024-01-14"
    }
    
    result = fill_pdf_with_numbers(test_data)
    print(result)