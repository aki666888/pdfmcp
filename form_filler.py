#!/usr/bin/env python3
"""
PharmaCare MACS Form Filler
Simple overlay approach with transparent text boxes
"""

import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class MACSFormFiller:
    def __init__(self, form_image_path):
        self.root = tk.Tk()
        self.root.title("PharmaCare MACS Form Filler")
        
        # Load form image
        self.form_image_path = form_image_path
        self.load_form_image()
        
        # Field coordinates (x, y, width, height) - adjusted for actual form layout
        self.fields = {
            'patient_name': (95, 80, 200, 20),
            'phn': (350, 80, 150, 20),
            'phone': (550, 80, 150, 20),
            'symptoms': (30, 295, 680, 40),  # Patient symptoms and signs
            'medical_history': (30, 360, 680, 30),  # Below "no interactions with current medication profile"
            'diagnosis': (30, 400, 680, 30),
            # Recommendations box is below "Medication,sig,mitte,refills:" line
            'medication_details': (30, 490, 680, 40),
            # Date field at bottom right (only date changes)
            'date_signed': (500, 750, 100, 20)
        }
        
        # Pre-checked items (always checked)
        self.pharmanet_checked = True
        self.patient_eligible = True
        self.informed_consent = True
        
        # Constants (pre-filled on form):
        # - Pharmacy: Tablet Pharmacy 3
        # - Address: 101-6373 Hammond Bay Rd, Nanaimo BC, V9S1Y1
        # - Pharmacist: Aki Shah #14901
        # - Signature: Already on form
        # - Follow-up: "will be followed up in 5 days time" (constant text)
        
        # Create transparent overlay entries
        self.entries = {}
        self.create_overlay_entries()
        
        # Create control panel
        self.create_control_panel()
        
    def load_form_image(self):
        """Load and display the form image"""
        image = Image.open(self.form_image_path)
        # Resize if needed
        self.photo = ImageTk.PhotoImage(image)
        
        # Create canvas for the form
        self.canvas = tk.Canvas(self.root, width=image.width, height=image.height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
    def create_overlay_entries(self):
        """Create transparent entry fields over the form"""
        for field_name, (x, y, width, height) in self.fields.items():
            entry = tk.Entry(self.canvas, 
                           relief=tk.FLAT,
                           highlightthickness=1,
                           highlightcolor='blue',
                           bg='white',
                           fg='black',
                           font=('Arial', 10))
            
            # Place entry on canvas
            self.canvas.create_window(x, y, window=entry, anchor=tk.NW, 
                                     width=width, height=height)
            self.entries[field_name] = entry
            
    def create_control_panel(self):
        """Create side panel with controls"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(control_frame, text="MACS Form Filler", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Info label
        info_text = """Pre-checked items:
✓ Pharmacist checked
✓ Patient eligible  
✓ Informed consent

Pre-filled on form:
• Pharmacy: Tablet Pharmacy 3
• Pharmacist: Aki Shah #14901
• Follow-up: 5 days
• Signature: Preserved

Note: Minor ailments are NOT
pre-checked - select as needed"""
        ttk.Label(control_frame, text=info_text, 
                 font=('Arial', 9), justify=tk.LEFT).pack(pady=10, anchor=tk.W)
        
        # Condition checkboxes
        ttk.Label(control_frame, text="Common Conditions:").pack(anchor=tk.W)
        
        self.conditions = {
            'acne': tk.BooleanVar(),
            'allergic_rhinitis': tk.BooleanVar(),
            'uti': tk.BooleanVar(),
            'headache': tk.BooleanVar(),
            'dermatitis': tk.BooleanVar()
        }
        
        for condition, var in self.conditions.items():
            ttk.Checkbutton(control_frame, 
                          text=condition.replace('_', ' ').title(),
                          variable=var).pack(anchor=tk.W)
        
        # Buttons
        ttk.Button(control_frame, text="Fill Sample Data",
                  command=self.fill_sample_data).pack(pady=10, fill=tk.X)
        
        ttk.Button(control_frame, text="Clear All",
                  command=self.clear_all).pack(pady=5, fill=tk.X)
        
        ttk.Button(control_frame, text="Save to JSON",
                  command=self.save_to_json).pack(pady=5, fill=tk.X)
        
        ttk.Button(control_frame, text="Load from JSON",
                  command=self.load_from_json).pack(pady=5, fill=tk.X)
        
        # Prescription checkbox
        self.prescription_issued = tk.BooleanVar()
        ttk.Checkbutton(control_frame, text="Prescription Issued",
                       variable=self.prescription_issued).pack(pady=10)
        
    def fill_sample_data(self):
        """Fill form with sample data"""
        self.entries['patient_name'].delete(0, tk.END)
        self.entries['patient_name'].insert(0, "John Doe")
        
        self.entries['phn'].delete(0, tk.END)
        self.entries['phn'].insert(0, "9876543210")
        
        self.entries['phone'].delete(0, tk.END)
        self.entries['phone'].insert(0, "(250) 555-0123")
        
        self.entries['symptoms'].delete(0, tk.END)
        self.entries['symptoms'].insert(0, "Patient presents with mild headache, duration 2 days")
        
        self.entries['medical_history'].delete(0, tk.END)
        self.entries['medical_history'].insert(0, "No significant PMHx. No drug allergies.")
        
        self.entries['diagnosis'].delete(0, tk.END)
        self.entries['diagnosis'].insert(0, "Tension headache")
        
        self.entries['medication_details'].delete(0, tk.END)
        self.entries['medication_details'].insert(0, "Acetaminophen 500mg PO q4-6h PRN #30 Refills: 0")
        
        # Set today's date
        from datetime import datetime
        self.entries['date_signed'].delete(0, tk.END)
        self.entries['date_signed'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        
    def clear_all(self):
        """Clear all fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        for var in self.conditions.values():
            var.set(False)
        self.prescription_issued.set(False)
        
    def get_form_data(self):
        """Get all form data as dictionary"""
        data = {
            'patient_info': {
                'name': self.entries['patient_name'].get(),
                'phn': self.entries['phn'].get(),
                'phone': self.entries['phone'].get()
            },
            'assessment': {
                'symptoms': self.entries['symptoms'].get(),
                'diagnosis': self.entries['diagnosis'].get()
            },
            'recommendations': self.entries['recommendations'].get(),
            'conditions': {k: v.get() for k, v in self.conditions.items()},
            'prescription_issued': self.prescription_issued.get(),
            'provider_info': {
                'name': self.entries['provider_name'].get(),
                'date_notified': self.entries['date_notified'].get(),
                'method': self.entries['method_notified'].get()
            },
            'timestamp': datetime.now().isoformat()
        }
        return data
        
    def save_to_json(self):
        """Save form data to JSON file"""
        data = self.get_form_data()
        filename = f"macs_form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        messagebox.showinfo("Success", f"Form data saved to {filename}")
        
    def load_from_json(self):
        """Load form data from JSON file"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            # Fill the form
            self.entries['patient_name'].delete(0, tk.END)
            self.entries['patient_name'].insert(0, data['patient_info']['name'])
            
            self.entries['phn'].delete(0, tk.END)
            self.entries['phn'].insert(0, data['patient_info']['phn'])
            
            self.entries['phone'].delete(0, tk.END)
            self.entries['phone'].insert(0, data['patient_info']['phone'])
            
            self.entries['symptoms'].delete(0, tk.END)
            self.entries['symptoms'].insert(0, data['assessment']['symptoms'])
            
            self.entries['diagnosis'].delete(0, tk.END)
            self.entries['diagnosis'].insert(0, data['assessment']['diagnosis'])
            
            self.entries['recommendations'].delete(0, tk.END)
            self.entries['recommendations'].insert(0, data['recommendations'])
            
            # Set conditions
            for condition, value in data['conditions'].items():
                if condition in self.conditions:
                    self.conditions[condition].set(value)
                    
            self.prescription_issued.set(data.get('prescription_issued', False))
            
    def run(self):
        """Run the application"""
        self.root.mainloop()
        
    def fill_from_args(self, patient_name=None, condition=None, phn=None, phone=None):
        """Fill form from command line arguments"""
        if patient_name:
            self.entries['patient_name'].delete(0, tk.END)
            self.entries['patient_name'].insert(0, patient_name)
            
        if phn:
            self.entries['phn'].delete(0, tk.END)
            self.entries['phn'].insert(0, phn)
            
        if phone:
            self.entries['phone'].delete(0, tk.END)
            self.entries['phone'].insert(0, phone)
            
        if condition and condition.lower().replace(' ', '_') in self.conditions:
            self.conditions[condition.lower().replace(' ', '_')].set(True)

def main():
    """Main entry point for command line usage"""
    # Default form image path
    form_image = r"C:\mcp-servers\pharmacare-form\blank.jpg"
    
    # Check if form image exists
    if not os.path.exists(form_image):
        print(f"Error: Form image not found at {form_image}")
        sys.exit(1)
        
    # Create form filler
    app = MACSFormFiller(form_image)
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        # Parse arguments
        patient_name = sys.argv[1] if len(sys.argv) > 1 else None
        condition = sys.argv[2] if len(sys.argv) > 2 else None
        phn = sys.argv[3] if len(sys.argv) > 3 else None
        phone = sys.argv[4] if len(sys.argv) > 4 else None
        
        # Fill form with provided data
        app.root.after(100, lambda: app.fill_from_args(patient_name, condition, phn, phone))
    
    # Run the application
    app.run()

if __name__ == "__main__":
    main()