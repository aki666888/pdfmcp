#!/usr/bin/env python3
"""
Enhanced PharmaCare MACS Form with Auto-fill and Save
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys

class EnhancedMACSForm:
    def __init__(self, initial_data=None):
        self.root = tk.Tk()
        self.root.title("PharmaCare MACS Form - Enhanced")
        self.root.geometry("900x800")
        
        # Store initial data
        self.initial_data = initial_data or {}
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(main_frame, text="PharmaCare MACS Form", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Pre-checked items label
        ttk.Label(main_frame, text="✓ Pharmacist Checked  ✓ Patient Eligible  ✓ Informed Consent", 
                 font=('Arial', 10, 'bold'), foreground='green').grid(row=1, column=0, columnspan=3, pady=5)
        
        # Create sections
        self.create_patient_section(main_frame, 2)
        self.create_conditions_section(main_frame, 5)
        self.create_assessment_section(main_frame, 8)
        self.create_buttons_section(main_frame, 14)
        
        # Auto-fill if data provided
        if self.initial_data:
            self.auto_fill()
        
    def create_patient_section(self, parent, start_row):
        """Create patient information section"""
        ttk.Label(parent, text="Patient Information", 
                 font=('Arial', 12, 'bold')).grid(row=start_row, column=0, columnspan=3, pady=5, sticky=tk.W)
        
        # Name
        ttk.Label(parent, text="Patient Name:").grid(row=start_row+1, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(parent, width=40)
        self.name_entry.grid(row=start_row+1, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        # PHN
        ttk.Label(parent, text="PHN:").grid(row=start_row+2, column=0, sticky=tk.W, pady=2)
        self.phn_entry = ttk.Entry(parent, width=40)
        self.phn_entry.grid(row=start_row+2, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        # Phone
        ttk.Label(parent, text="Phone:").grid(row=start_row+3, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(parent, width=40)
        self.phone_entry.grid(row=start_row+3, column=1, columnspan=2, sticky=tk.W, pady=2)
        
    def create_conditions_section(self, parent, start_row):
        """Create conditions section"""
        ttk.Label(parent, text="Minor Ailments (select as needed)", 
                 font=('Arial', 12, 'bold')).grid(row=start_row, column=0, columnspan=3, pady=10, sticky=tk.W)
        
        conditions_frame = ttk.LabelFrame(parent, text="Select Conditions", padding="5")
        conditions_frame.grid(row=start_row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.conditions = {}
        condition_list = [
            ("Acne", "acne"), ("Allergic Rhinitis", "allergic_rhinitis"),
            ("Headache", "headache"), ("UTI", "uti"),
            ("Dermatitis", "dermatitis"), ("Fungal Infection", "fungal_infection"),
            ("Herpes Labialis", "herpes_labialis"), ("Impetigo", "impetigo")
        ]
        
        for i, (label, key) in enumerate(condition_list):
            var = tk.BooleanVar()
            self.conditions[key] = var
            ttk.Checkbutton(conditions_frame, text=label, variable=var).grid(
                row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
                
    def create_assessment_section(self, parent, start_row):
        """Create assessment section"""
        ttk.Label(parent, text="Patient Assessment", 
                 font=('Arial', 12, 'bold')).grid(row=start_row, column=0, columnspan=3, pady=10, sticky=tk.W)
        
        # Symptoms
        ttk.Label(parent, text="Symptoms & Signs:").grid(row=start_row+1, column=0, sticky=tk.NW, pady=2)
        self.symptoms_text = tk.Text(parent, width=60, height=3)
        self.symptoms_text.grid(row=start_row+1, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        # Medical History
        ttk.Label(parent, text="Medical History:").grid(row=start_row+2, column=0, sticky=tk.NW, pady=2)
        self.medical_history_text = tk.Text(parent, width=60, height=2)
        self.medical_history_text.grid(row=start_row+2, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        # Diagnosis
        ttk.Label(parent, text="Diagnosis:").grid(row=start_row+3, column=0, sticky=tk.W, pady=2)
        self.diagnosis_entry = ttk.Entry(parent, width=50)
        self.diagnosis_entry.grid(row=start_row+3, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        # Medication
        ttk.Label(parent, text="Medication (sig, mitte, refills):").grid(row=start_row+4, column=0, sticky=tk.NW, pady=2)
        self.medication_text = tk.Text(parent, width=60, height=2)
        self.medication_text.grid(row=start_row+4, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        # Prescription checkbox
        self.prescription_var = tk.BooleanVar()
        ttk.Checkbutton(parent, text="Prescription Issued", 
                       variable=self.prescription_var).grid(row=start_row+5, column=0, columnspan=3, pady=10)
                       
    def create_buttons_section(self, parent, start_row):
        """Create buttons section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=start_row, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Save as PDF", 
                  command=self.save_as_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save as Image", 
                  command=self.save_as_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Data (JSON)", 
                  command=self.save_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
                  
    def auto_fill(self):
        """Auto-fill form with provided data"""
        if 'patient_name' in self.initial_data:
            self.name_entry.insert(0, self.initial_data['patient_name'])
        if 'phn' in self.initial_data:
            self.phn_entry.insert(0, self.initial_data['phn'])
        if 'phone' in self.initial_data:
            self.phone_entry.insert(0, self.initial_data['phone'])
        if 'symptoms' in self.initial_data:
            self.symptoms_text.insert(1.0, self.initial_data['symptoms'])
        if 'medical_history' in self.initial_data:
            self.medical_history_text.insert(1.0, self.initial_data['medical_history'])
        if 'diagnosis' in self.initial_data:
            self.diagnosis_entry.insert(0, self.initial_data['diagnosis'])
        if 'medication' in self.initial_data:
            self.medication_text.insert(1.0, self.initial_data['medication'])
        if 'condition' in self.initial_data and self.initial_data['condition'] in self.conditions:
            self.conditions[self.initial_data['condition']].set(True)
            
    def get_patient_folder(self):
        """Get patient folder name"""
        patient_name = self.name_entry.get()
        if not patient_name:
            return None
            
        # Extract first name or last name
        folder_name = patient_name.split(',')[0].strip() if ',' in patient_name else patient_name.split()[0]
        folder_name = "".join(c for c in folder_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return folder_name
        
    def save_as_pdf(self):
        """Save form as PDF"""
        folder_name = self.get_patient_folder()
        if not folder_name:
            messagebox.showerror("Error", "Please enter patient name")
            return
            
        save_dir = f"C:/forms/{folder_name}"
        os.makedirs(save_dir, exist_ok=True)
        
        # Create the filled form image
        filled_image = self.create_filled_form_image()
        
        # Save as PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(save_dir, f"MACS_Form_{folder_name}_{timestamp}.pdf")
        filled_image.save(pdf_path, "PDF", resolution=100.0)
        
        messagebox.showinfo("Success", f"Form saved as PDF:\n{pdf_path}")
        
    def save_as_image(self):
        """Save form as image"""
        folder_name = self.get_patient_folder()
        if not folder_name:
            messagebox.showerror("Error", "Please enter patient name")
            return
            
        save_dir = f"C:/forms/{folder_name}"
        os.makedirs(save_dir, exist_ok=True)
        
        # Create the filled form image
        filled_image = self.create_filled_form_image()
        
        # Save as PNG
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(save_dir, f"MACS_Form_{folder_name}_{timestamp}.png")
        filled_image.save(img_path, "PNG")
        
        messagebox.showinfo("Success", f"Form saved as image:\n{img_path}")
        
    def create_filled_form_image(self):
        """Create a filled form image"""
        # Load blank form
        form_path = r"C:\mcp-servers\pharmacare-form\blank.jpg"
        if not os.path.exists(form_path):
            form_path = r"C:\Users\info0\Downloads\blank_page-0001 (1).jpg"
            
        img = Image.open(form_path)
        draw = ImageDraw.Draw(img)
        
        # Try to load font
        try:
            font = ImageFont.truetype("arial.ttf", 14)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            small_font = font
            
        # Add text to form (adjust positions as needed)
        draw.text((95, 80), self.name_entry.get(), fill='black', font=font)
        draw.text((350, 80), self.phn_entry.get(), fill='black', font=font)
        draw.text((550, 80), self.phone_entry.get(), fill='black', font=font)
        
        # Add symptoms (with text wrapping)
        symptoms = self.symptoms_text.get(1.0, tk.END).strip()
        y_pos = 295
        for line in symptoms.split('\n'):
            if line:
                draw.text((30, y_pos), line[:80], fill='black', font=small_font)
                y_pos += 15
                
        # Add other fields
        draw.text((30, 360), self.medical_history_text.get(1.0, tk.END).strip()[:80], fill='black', font=small_font)
        draw.text((30, 400), self.diagnosis_entry.get(), fill='black', font=font)
        draw.text((30, 490), self.medication_text.get(1.0, tk.END).strip()[:80], fill='black', font=font)
        
        # Add date
        draw.text((500, 750), datetime.now().strftime("%Y-%m-%d"), fill='black', font=font)
        
        # Add checkmarks
        draw.text((42, 273), "✓", fill='black', font=font)  # Pharmacist
        draw.text((160, 273), "✓", fill='black', font=font)  # Eligible
        
        return img
        
    def save_json(self):
        """Save form data as JSON"""
        folder_name = self.get_patient_folder()
        if not folder_name:
            messagebox.showerror("Error", "Please enter patient name")
            return
            
        save_dir = f"C:/forms/{folder_name}"
        os.makedirs(save_dir, exist_ok=True)
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "patient_info": {
                "name": self.name_entry.get(),
                "phn": self.phn_entry.get(),
                "phone": self.phone_entry.get()
            },
            "conditions": {k: v.get() for k, v in self.conditions.items()},
            "assessment": {
                "symptoms": self.symptoms_text.get(1.0, tk.END).strip(),
                "medical_history": self.medical_history_text.get(1.0, tk.END).strip(),
                "diagnosis": self.diagnosis_entry.get()
            },
            "medication": self.medication_text.get(1.0, tk.END).strip(),
            "prescription_issued": self.prescription_var.get()
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(save_dir, f"MACS_Form_{folder_name}_{timestamp}.json")
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        messagebox.showinfo("Success", f"Data saved:\n{json_path}")
        
    def clear_all(self):
        """Clear all fields"""
        self.name_entry.delete(0, tk.END)
        self.phn_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.symptoms_text.delete(1.0, tk.END)
        self.medical_history_text.delete(1.0, tk.END)
        self.diagnosis_entry.delete(0, tk.END)
        self.medication_text.delete(1.0, tk.END)
        for var in self.conditions.values():
            var.set(False)
        self.prescription_var.set(False)
        
    def run(self):
        self.root.mainloop()

# Entry point for MCP
def launch_form(data=None):
    """Launch form with optional data"""
    app = EnhancedMACSForm(initial_data=data)
    app.run()

if __name__ == "__main__":
    # Test with command line args
    if len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
            launch_form(data)
        except:
            launch_form()
    else:
        launch_form()