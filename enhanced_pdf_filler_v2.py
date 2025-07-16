#!/usr/bin/env python3
"""
Enhanced PDF Filler V2 - Proper Text Wrapping Fix
Using correct PyMuPDF insert_textbox syntax for reliable wrapping
"""
import os
import json
import fitz  # PyMuPDF
from datetime import datetime
import logging

class EnhancedPDFFiller:
    def __init__(self):
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Try to find mapping file
        mapping_paths = [
            r"C:\mcp-servers\pharmacare-form\macs_form_mapping_v3.json",
            r"C:\forms\macs_form_mapping_v3_updated.json",
            r"C:\forms\macs_form_mapping_v3.json",
            "macs_form_mapping_v3_updated.json",
            "macs_form_mapping_v3.json"
        ]
        
        self.mapping = None
        for path in mapping_paths:
            if os.path.exists(path):
                self.logger.info(f"Loading mapping from: {path}")
                with open(path, 'r') as f:
                    self.mapping = json.load(f)
                break
        
        if not self.mapping:
            raise FileNotFoundError("No mapping file found in any of the expected locations")
    
    def fill_form(self, data):
        """Fill the PDF form with provided data"""
        try:
            # Determine PDF path
            pdf_filename = self.mapping.get('pdf_file', 'blank.pdf')
            pdf_paths = [
                os.path.join(r"C:\mcp-servers\pharmacare-form", pdf_filename),
                os.path.join(r"C:\forms", pdf_filename),
                pdf_filename
            ]
            
            pdf_path = None
            for path in pdf_paths:
                if os.path.exists(path):
                    pdf_path = path
                    break
            
            if not pdf_path:
                raise FileNotFoundError(f"PDF file {pdf_filename} not found")
            
            self.logger.info(f"Opening PDF: {pdf_path}")
            doc = fitz.open(pdf_path)
            
            # Handle condition boxes first
            condition_numbers = data.get('condition_numbers', [])
            if isinstance(condition_numbers, int):
                condition_numbers = [condition_numbers]
            elif isinstance(condition_numbers, str):
                # Parse string like "1,3,5" or "1 3 5"
                condition_numbers = [int(x.strip()) for x in condition_numbers.replace(',', ' ').split() if x.strip().isdigit()]
            
            # Highlight condition boxes
            for page_num in range(len(doc)):
                page = doc[page_num]
                for box_num in condition_numbers:
                    self._highlight_condition_box(page, box_num)
            
            # Process each field
            for field_name, field_data in data.items():
                if field_name in self.mapping['fields']:
                    self._fill_field(doc, field_name, field_data)
            
            # Save output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create output directory if needed
            output_dir = r"C:\forms"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename with full patient name
            patient_name = data.get('patient_name', 'Unknown')
            safe_patient_name = patient_name.replace(' ', '_').replace(',', '')
            output_filename = f"{safe_patient_name}_{timestamp}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            doc.save(output_path)
            doc.close()
            
            self.logger.info(f"Form saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error filling form: {str(e)}")
            raise
    
    def _fill_field(self, doc, field_name, value):
        """Fill a specific field with proper text wrapping"""
        field_coords = self.mapping['fields'].get(field_name, [])
        
        for coord in field_coords:
            page_num = coord['page']
            page = doc[page_num]
            
            # Create rectangle from coordinates
            rect = fitz.Rect(coord['x1'], coord['y1'], coord['x2'], coord['y2'])
            
            # Special handling for different field types
            if field_name == "symptoms":
                # For symptoms field - smaller font, tighter spacing
                fontsize = 6
                # Try to insert text with automatic wrapping
                rc = page.insert_textbox(
                    rect,
                    str(value),
                    fontname="helv",
                    fontsize=fontsize,
                    align=fitz.TEXT_ALIGN_LEFT
                )
                
                # If text doesn't fit, try progressively smaller font sizes
                while rc < 0 and fontsize > 4:
                    fontsize -= 0.5
                    rc = page.insert_textbox(
                        rect,
                        str(value),
                        fontname="helv",
                        fontsize=fontsize,
                        align=fitz.TEXT_ALIGN_LEFT
                    )
                
                if rc < 0:
                    # If still doesn't fit, truncate and add ellipsis
                    truncated = self._truncate_text(str(value), rect, page, fontsize)
                    page.insert_textbox(
                        rect,
                        truncated,
                        fontname="helv",
                        fontsize=fontsize,
                        align=fitz.TEXT_ALIGN_LEFT
                    )
                    self.logger.warning(f"Text truncated for field {field_name}")
                    
            elif field_name in ["date", "doctor_name", "patient_name"]:
                # Regular fields - normal font size
                page.insert_textbox(
                    rect,
                    str(value),
                    fontname="helv",
                    fontsize=10,
                    align=fitz.TEXT_ALIGN_LEFT
                )
            else:
                # Default handling
                page.insert_textbox(
                    rect,
                    str(value),
                    fontname="helv",
                    fontsize=8,
                    align=fitz.TEXT_ALIGN_LEFT
                )
    
    def _truncate_text(self, text, rect, page, fontsize):
        """Truncate text to fit within rectangle"""
        # Try progressively shorter text until it fits
        truncated = text
        while len(truncated) > 10:
            test_text = truncated[:-10] + "..."
            rc = page.insert_textbox(
                rect,
                test_text,
                fontname="helv",
                fontsize=fontsize,
                align=fitz.TEXT_ALIGN_LEFT
            )
            if rc >= 0:
                return test_text
            truncated = truncated[:-10]
        return truncated[:10] + "..."
    
    def _highlight_condition_box(self, page, box_number):
        """Highlight a specific condition box by number"""
        for box in self.mapping.get('condition_boxes', []):
            if box['number'] == box_number:
                # Draw a red checkmark in the box
                check_x = box['x1'] + 5
                check_y = box['y1'] + 20
                
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

def handle_pdf_request(data):
    """Handle incoming PDF fill request"""
    try:
        filler = EnhancedPDFFiller()
        
        # Extract form data
        form_data = {}
        if 'patient_name' in data:
            form_data['patient_name'] = data['patient_name']
        if 'doctor_name' in data:
            form_data['doctor_name'] = data['doctor_name']
        # Always add date - use provided date or today's date
        form_data['date'] = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        if 'symptoms' in data:
            form_data['symptoms'] = data['symptoms']
        
        # Add any other fields from data
        for key, value in data.items():
            if key not in form_data:
                form_data[key] = value
        
        # Fill the form
        output_path = filler.fill_form(form_data)
        
        return {
            "success": True,
            "message": "Form filled successfully",
            "output_path": output_path
        }
        
    except Exception as e:
        logging.error(f"Error in handle_pdf_request: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test with sample data
    test_data = {
        'patient_name': 'John Smith',
        'doctor_name': 'Dr. Jane Wilson',
        'date': '2024-03-20',
        'symptoms': """Patient presents with severe headache lasting 3 days, accompanied by nausea and photophobia. 
        Temperature 38.5°C, blood pressure 130/85. Patient reports difficulty sleeping and loss of appetite. 
        Previous history of migraines but this episode is more severe than usual. No recent trauma or injury. 
        Family history includes hypertension and diabetes. Currently taking ibuprofen 400mg as needed. 
        Allergic to penicillin. Requests further evaluation and treatment options. 
        Additional symptoms include dizziness when standing and mild neck stiffness."""
    }
    
    result = handle_pdf_request(test_data)
    print(json.dumps(result, indent=2))