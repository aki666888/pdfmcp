#!/usr/bin/env python3
"""
Direct PDF Form Filler for PharmaCare MACS
Fills existing fillable PDF forms directly
"""

import os
import json
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter

class PDFFormFiller:
    def __init__(self):
        self.blank_pdf_path = r"C:\Users\info0\Downloads\blank.pdf"
        
        # Field mappings - update these based on actual PDF field names
        self.field_mappings = {
            # Patient Information
            'patient_name': 'PatientName',  # Update with actual field name
            'phn': 'PHN',  # Update with actual field name
            'phone': 'PhoneNumber',  # Update with actual field name
            
            # Checkboxes (pre-checked)
            'pharmacist_checked': 'PharmacistChecked',
            'patient_eligible': 'PatientEligible',
            'informed_consent': 'InformedConsent',
            
            # Conditions checkboxes
            'acne': 'Acne',
            'allergic_rhinitis': 'AllergicRhinitis',
            'headache': 'Headache',
            'uti': 'UTI',
            'dermatitis': 'Dermatitis',
            'fungal_infection': 'FungalInfection',
            'herpes_labialis': 'HerpesLabialis',
            'impetigo': 'Impetigo',
            
            # Assessment fields
            'symptoms': 'Symptoms',
            'medical_history': 'MedicalHistory',
            'diagnosis': 'Diagnosis',
            
            # Medication
            'medication': 'Medication',
            
            # Date
            'date': 'Date',
            
            # Prescription checkbox
            'prescription_issued': 'PrescriptionIssued'
        }
    
    def get_pdf_fields(self):
        """Get all field names from the PDF to help with mapping"""
        try:
            reader = PdfReader(self.blank_pdf_path)
            fields = reader.get_form_text_fields()
            
            print("Available PDF form fields:")
            for field_name, field_value in fields.items():
                print(f"  {field_name}: {field_value}")
            
            return list(fields.keys())
        except Exception as e:
            print(f"Error reading PDF fields: {e}")
            return []
    
    def fill_pdf(self, data):
        """Fill the PDF form with provided data"""
        try:
            # Read the blank PDF
            reader = PdfReader(self.blank_pdf_path)
            writer = PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Fill form fields
            writer.update_page_form_field_values(
                writer.pages[0], 
                self._prepare_field_data(data)
            )
            
            # Create output directory
            patient_name = data.get("patient_name", "Unknown")
            patient_folder = patient_name.split(',')[0].strip() if ',' in patient_name else patient_name.split()[0]
            patient_folder = "".join(c for c in patient_folder if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            save_dir = f"C:/forms/{patient_folder}"
            os.makedirs(save_dir, exist_ok=True)
            
            # Save filled PDF
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.pdf")
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Also save JSON data
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
    
    def _prepare_field_data(self, data):
        """Prepare data for PDF form fields"""
        field_data = {}
        
        # Basic fields
        field_data[self.field_mappings['patient_name']] = data.get('patient_name', '')
        field_data[self.field_mappings['phn']] = data.get('phn', '')
        field_data[self.field_mappings['phone']] = data.get('phone', '')
        
        # Pre-checked items
        field_data[self.field_mappings['pharmacist_checked']] = '/Yes'
        field_data[self.field_mappings['patient_eligible']] = '/Yes'
        field_data[self.field_mappings['informed_consent']] = '/Yes'
        
        # Condition checkbox
        condition = data.get('condition', '').lower()
        if condition in self.field_mappings:
            field_data[self.field_mappings[condition]] = '/Yes'
        
        # Text fields
        field_data[self.field_mappings['symptoms']] = data.get('symptoms', '')
        field_data[self.field_mappings['medical_history']] = data.get('medical_history', '')
        field_data[self.field_mappings['diagnosis']] = data.get('diagnosis', '')
        field_data[self.field_mappings['medication']] = data.get('medication', '')
        
        # Date
        field_data[self.field_mappings['date']] = datetime.now().strftime("%Y-%m-%d")
        
        # Prescription issued
        if data.get('prescription_issued', False):
            field_data[self.field_mappings['prescription_issued']] = '/Yes'
        
        return field_data

# Fast function for MCP
def fill_fillable_pdf(data):
    """Quick PDF fill function"""
    filler = PDFFormFiller()
    
    # First, let's discover the actual field names
    # filler.get_pdf_fields()  # Uncomment to see field names
    
    result = filler.fill_pdf(data)
    
    if result["success"]:
        return f"Form saved successfully!\nPDF: {result['pdf_path']}\nData: {result['json_path']}"
    else:
        return f"Error: {result['error']}"

# Test to discover field names
if __name__ == "__main__":
    filler = PDFFormFiller()
    
    # First run this to see what fields are in the PDF
    print("Discovering PDF field names...")
    filler.get_pdf_fields()
    
    # Then test with sample data
    # test_data = {
    #     "patient_name": "Test Patient",
    #     "phn": "1234567890",
    #     "phone": "(250) 555-0123",
    #     "condition": "headache",
    #     "symptoms": "Test symptoms",
    #     "medical_history": "No allergies",
    #     "diagnosis": "Test diagnosis",
    #     "medication": "Test medication",
    #     "prescription_issued": True
    # }
    # 
    # result = fill_fillable_pdf(test_data)
    # print(result)