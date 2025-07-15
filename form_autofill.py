#!/usr/bin/env python3
"""
Auto-fill and save PharmaCare MACS form
"""

import os
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time

def fill_and_save_form(form_data):
    """Fill the form with data and save as PDF/image"""
    
    try:
        # Extract data
        patient_name = form_data.get("patient_name", "")
        phn = form_data.get("phn", "")
        phone = form_data.get("phone", "")
        condition = form_data.get("condition", "")
        symptoms = form_data.get("symptoms", "")
        medical_history = form_data.get("medical_history", "")
        diagnosis = form_data.get("diagnosis", "")
        medication = form_data.get("medication", "")
        save_pdf = form_data.get("save_pdf", True)
        
        # Create patient folder
        patient_folder = patient_name.split(',')[0].strip() if ',' in patient_name else patient_name.split()[0]
        patient_folder = "".join(c for c in patient_folder if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        save_dir = f"C:/forms/{patient_folder}"
        os.makedirs(save_dir, exist_ok=True)
        
        # Load the blank form image
        form_image_path = r"C:\mcp-servers\pharmacare-form\blank.jpg"
        if not os.path.exists(form_image_path):
            # Try the original path
            form_image_path = r"C:\Users\info0\Downloads\blank_page-0001 (1).jpg"
        
        if not os.path.exists(form_image_path):
            return f"Error: Form image not found at {form_image_path}"
        
        # Open image
        img = Image.open(form_image_path)
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 14)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Define text positions (x, y) for each field
        # These are approximate positions based on the form layout
        positions = {
            'patient_name': (95, 80),
            'phn': (350, 80),
            'phone': (550, 80),
            'symptoms': (30, 295),
            'medical_history': (30, 360),
            'diagnosis': (30, 400),
            'medication': (30, 490),
            'date': (500, 750)
        }
        
        # Fill in the text
        draw.text(positions['patient_name'], patient_name, fill='black', font=font)
        draw.text(positions['phn'], phn, fill='black', font=font)
        draw.text(positions['phone'], phone, fill='black', font=font)
        
        # Wrap long text for symptoms
        if symptoms:
            y_offset = 0
            words = symptoms.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if len(test_line) > 80:  # Approximate line length
                    draw.text((positions['symptoms'][0], positions['symptoms'][1] + y_offset), 
                             line.strip(), fill='black', font=small_font)
                    line = word + " "
                    y_offset += 15
                else:
                    line = test_line
            if line:
                draw.text((positions['symptoms'][0], positions['symptoms'][1] + y_offset), 
                         line.strip(), fill='black', font=small_font)
        
        if medical_history:
            draw.text(positions['medical_history'], medical_history, fill='black', font=small_font)
        
        if diagnosis:
            draw.text(positions['diagnosis'], diagnosis, fill='black', font=font)
        
        if medication:
            draw.text(positions['medication'], medication, fill='black', font=font)
        
        # Add date
        draw.text(positions['date'], datetime.now().strftime("%Y-%m-%d"), fill='black', font=font)
        
        # Draw checkmarks for pre-checked items (approximate positions)
        checkmark = "✓"
        draw.text((42, 273), checkmark, fill='black', font=font)  # Pharmacist checked
        draw.text((160, 273), checkmark, fill='black', font=font)  # Patient eligible
        
        # Check the appropriate condition box
        condition_positions = {
            'headache': (315, 128),
            'uti': (205, 336),
            'acne': (42, 142),
            'allergic_rhinitis': (42, 156),
            'dermatitis': (42, 184),
            'fungal_infection': (160, 170),
            'herpes_labialis': (315, 156),
            'impetigo': (315, 170)
        }
        
        if condition and condition.lower() in condition_positions:
            pos = condition_positions[condition.lower()]
            draw.text(pos, checkmark, fill='black', font=font)
        
        # Save the form
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if save_pdf:
            # Save as PDF
            pdf_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.pdf")
            img.save(pdf_path, "PDF", resolution=100.0)
            
            # Also save as PNG for backup
            png_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.png")
            img.save(png_path, "PNG")
            
            # Save JSON data
            json_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.json")
            with open(json_path, 'w') as f:
                json.dump({
                    "form_data": form_data,
                    "timestamp": timestamp,
                    "files": {
                        "pdf": pdf_path,
                        "png": png_path
                    }
                }, f, indent=2)
            
            return f"Form saved successfully!\nPDF: {pdf_path}\nPNG: {png_path}\nData: {json_path}"
        else:
            # Just save as image
            img_path = os.path.join(save_dir, f"MACS_Form_{patient_folder}_{timestamp}.png")
            img.save(img_path, "PNG")
            
            return f"Form saved as image: {img_path}"
            
    except Exception as e:
        return f"Error processing form: {str(e)}"

# Quick test function
if __name__ == "__main__":
    test_data = {
        "patient_name": "Test Patient",
        "phn": "1234567890",
        "phone": "(250) 555-0123",
        "condition": "headache",
        "symptoms": "Test symptoms",
        "medical_history": "No allergies",
        "diagnosis": "Test diagnosis",
        "medication": "Test medication",
        "save_pdf": True
    }
    
    result = fill_and_save_form(test_data)
    print(result)