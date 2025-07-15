#!/usr/bin/env python3
"""
Fast PharmaCare MACS Form Filler
Optimized for speed - directly fills and saves without GUI
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class FastFormFiller:
    def __init__(self):
        # Pre-load the form image
        self.form_path = r"C:\mcp-servers\pharmacare-form\blank.jpg"
        if not os.path.exists(self.form_path):
            self.form_path = r"C:\Users\info0\Downloads\blank_page-0001 (1).jpg"
        
        # Try to load font once
        try:
            self.font = ImageFont.truetype("arial.ttf", 14)
            self.small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            self.font = ImageFont.load_default()
            self.small_font = self.font
            
        # Field positions
        self.positions = {
            'patient_name': (95, 80),
            'phn': (350, 80),
            'phone': (550, 80),
            'symptoms': (30, 295),
            'medical_history': (30, 360),
            'diagnosis': (30, 400),
            'medication': (30, 490),
            'date': (500, 750),
            # Checkmark positions
            'pharmanet': (42, 273),
            'eligible': (160, 273),
            'consent': (577, 97)  # Informed consent position
        }
        
        # Condition checkbox positions
        self.condition_positions = {
            'headache': (315, 128),
            'uti': (205, 336),
            'acne': (42, 142),
            'allergic_rhinitis': (42, 156),
            'dermatitis': (42, 184),
            'fungal_infection': (160, 170),
            'herpes_labialis': (315, 156),
            'impetigo': (315, 170)
        }
        
    def fill_form(self, data):
        """Fill form with data and save"""
        try:
            # Open a fresh copy of the image
            img = Image.open(self.form_path).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Extract data
            patient_name = data.get("patient_name", "")
            phn = data.get("phn", "")
            phone = data.get("phone", "")
            condition = data.get("condition", "")
            symptoms = data.get("symptoms", "")
            medical_history = data.get("medical_history", "")
            diagnosis = data.get("diagnosis", "")
            medication = data.get("medication", "")
            
            # Fill basic fields
            draw.text(self.positions['patient_name'], patient_name, fill='black', font=self.font)
            draw.text(self.positions['phn'], phn, fill='black', font=self.font)
            draw.text(self.positions['phone'], phone, fill='black', font=self.font)
            
            # Fill text areas with wrapping
            self._draw_wrapped_text(draw, symptoms, self.positions['symptoms'], 680, 40)
            self._draw_wrapped_text(draw, medical_history, self.positions['medical_history'], 680, 30)
            draw.text(self.positions['diagnosis'], diagnosis, fill='black', font=self.font)
            self._draw_wrapped_text(draw, medication, self.positions['medication'], 680, 40)
            
            # Add date
            draw.text(self.positions['date'], datetime.now().strftime("%Y-%m-%d"), fill='black', font=self.font)
            
            # Add checkmarks for pre-checked items
            checkmark = "✓"
            draw.text(self.positions['pharmanet'], checkmark, fill='black', font=self.font)
            draw.text(self.positions['eligible'], checkmark, fill='black', font=self.font)
            draw.text(self.positions['consent'], checkmark, fill='black', font=self.font)
            
            # Check condition box if specified
            if condition and condition.lower() in self.condition_positions:
                pos = self.condition_positions[condition.lower()]
                draw.text(pos, checkmark, fill='black', font=self.font)
            
            # Create patient folder
            patient_folder = patient_name.split(',')[0].strip() if ',' in patient_name else patient_name.split()[0]
            patient_folder = "".join(c for c in patient_folder if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            save_dir = f"C:/forms/{patient_folder}"
            os.makedirs(save_dir, exist_ok=True)
            
            # Save files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save as PDF
            pdf_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.pdf")
            img.save(pdf_path, "PDF", resolution=100.0)
            
            # Save as PNG
            png_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.png")
            img.save(png_path, "PNG")
            
            # Save JSON data
            json_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.json")
            with open(json_path, 'w') as f:
                json.dump({
                    "form_data": data,
                    "timestamp": timestamp,
                    "files": {
                        "pdf": pdf_path,
                        "png": png_path
                    }
                }, f, indent=2)
            
            return {
                "success": True,
                "message": f"Form saved successfully!",
                "pdf": pdf_path,
                "png": png_path,
                "json": json_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    def _draw_wrapped_text(self, draw, text, position, max_width, max_height):
        """Draw text with word wrapping"""
        if not text:
            return
            
        x, y = position
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            # Approximate width check
            if len(test_line) * 7 > max_width:  # ~7 pixels per character
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        y_offset = 0
        for line in lines[:3]:  # Limit to 3 lines
            draw.text((x, y + y_offset), line, fill='black', font=self.small_font)
            y_offset += 15

# Global instance for speed
_filler = None

def get_filler():
    global _filler
    if _filler is None:
        _filler = FastFormFiller()
    return _filler

def fill_and_save_form(data):
    """Quick form fill function"""
    filler = get_filler()
    result = filler.fill_form(data)
    
    if result["success"]:
        return f"Form saved successfully!\nPDF: {result['pdf']}\nPNG: {result['png']}\nData: {result['json']}"
    else:
        return f"Error: {result['message']}"

# Test
if __name__ == "__main__":
    test_data = {
        "patient_name": "Isenor, Kristofor",
        "phn": "9079287326",
        "phone": "(250) 937-1689",
        "condition": "fungal_infection",
        "symptoms": "Fungal infection of feet with scaling and itching",
        "medical_history": "No contraindications noted",
        "diagnosis": "Tinea pedis",
        "medication": "Lamisil 1% cream, apply twice daily",
        "save_pdf": True
    }
    
    result = fill_and_save_form(test_data)
    print(result)