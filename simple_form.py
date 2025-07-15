#!/usr/bin/env python3
"""
Simple PharmaCare MACS Form Filler
No MCP dependencies - just a GUI overlay
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class SimpleMACSForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PharmaCare MACS Form - Quick Fill")
        self.root.geometry("600x800")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(main_frame, text="PharmaCare MACS Form", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Pre-checked items label
        ttk.Label(main_frame, text="✓ Pharmacist Checked  ✓ Patient Eligible  ✓ Informed Consent", 
                 font=('Arial', 10, 'bold'), foreground='green').grid(row=1, column=0, columnspan=2, pady=5)
        
        # Patient Information
        ttk.Label(main_frame, text="Patient Information", 
                 font=('Arial', 12, 'bold')).grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        # Name
        ttk.Label(main_frame, text="Patient Name:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # PHN
        ttk.Label(main_frame, text="PHN:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.phn_entry = ttk.Entry(main_frame, width=40)
        self.phn_entry.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # Phone
        ttk.Label(main_frame, text="Phone:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(main_frame, width=40)
        self.phone_entry.grid(row=5, column=1, sticky=tk.W, pady=2)
        
        # Minor Ailments
        ttk.Label(main_frame, text="Minor Ailments (select as needed - NOT pre-checked)", 
                 font=('Arial', 12, 'bold')).grid(row=6, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Common conditions frame
        conditions_frame = ttk.LabelFrame(main_frame, text="Select Conditions", padding="5")
        conditions_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.conditions = {}
        common_conditions = [
            "Acne", "Allergic Rhinitis", "Headache", "UTI", 
            "Dermatitis", "Fungal Infection", "Herpes Labialis", "Impetigo"
        ]
        
        for i, condition in enumerate(common_conditions):
            var = tk.BooleanVar()
            self.conditions[condition.lower().replace(' ', '_')] = var
            ttk.Checkbutton(conditions_frame, text=condition, variable=var).grid(
                row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
        
        # Assessment
        ttk.Label(main_frame, text="Patient Assessment", 
                 font=('Arial', 12, 'bold')).grid(row=8, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Symptoms
        ttk.Label(main_frame, text="Symptoms & Signs:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.symptoms_text = tk.Text(main_frame, width=50, height=3)
        self.symptoms_text.grid(row=9, column=1, sticky=tk.W, pady=2)
        
        # Medical History (below "no interactions with current medication profile" line)
        ttk.Label(main_frame, text="Medical History:").grid(row=10, column=0, sticky=tk.W, pady=2)
        ttk.Label(main_frame, text="(no interactions with\ncurrent medication profile)", 
                 font=('Arial', 8, 'italic')).grid(row=10, column=0, sticky=tk.W, pady=20)
        self.medical_history_text = tk.Text(main_frame, width=50, height=2)
        self.medical_history_text.grid(row=10, column=1, sticky=tk.W, pady=2)
        
        # Diagnosis
        ttk.Label(main_frame, text="Diagnosis:").grid(row=11, column=0, sticky=tk.W, pady=2)
        self.diagnosis_entry = ttk.Entry(main_frame, width=40)
        self.diagnosis_entry.grid(row=11, column=1, sticky=tk.W, pady=2)
        
        # Medication Details (sig, mitte, refills)
        ttk.Label(main_frame, text="Medication Details:").grid(row=12, column=0, sticky=tk.W, pady=2)
        ttk.Label(main_frame, text="(sig, mitte, refills)", 
                 font=('Arial', 8, 'italic')).grid(row=12, column=0, sticky=tk.W, pady=18)
        self.medication_text = tk.Text(main_frame, width=50, height=2)
        self.medication_text.grid(row=12, column=1, sticky=tk.W, pady=2)
        
        # Prescription
        self.prescription_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Prescription Issued", 
                       variable=self.prescription_var).grid(row=13, column=0, columnspan=2, pady=10)
        
        # Note about Provider section
        ttk.Label(main_frame, text="(Provider notification section will remain empty)", 
                 font=('Arial', 9, 'italic'), foreground='gray').grid(row=14, column=0, columnspan=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Quick Fill - Headache", 
                  command=self.fill_headache).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quick Fill - UTI", 
                  command=self.fill_uti).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save JSON", 
                  command=self.save_json).pack(side=tk.LEFT, padx=5)
        
        # Constants info
        constants_frame = ttk.LabelFrame(main_frame, text="Pre-filled Information", padding="5")
        constants_frame.grid(row=16, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(constants_frame, text="✓ Pharmacy: Tablet Pharmacy 3", 
                 font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(constants_frame, text="✓ Address: 101-6373 Hammond Bay Rd, Nanaimo BC, V9S1Y1", 
                 font=('Arial', 9)).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(constants_frame, text="✓ Pharmacist: Aki Shah #14901 (Signature on form)", 
                 font=('Arial', 9)).grid(row=2, column=0, sticky=tk.W)
        ttk.Label(constants_frame, text="✓ Follow-up: Will be followed up in 5 days time", 
                 font=('Arial', 9)).grid(row=3, column=0, sticky=tk.W)
        
        # Date field
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=17, column=0, columnspan=2, pady=5)
        ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(date_frame, width=15)
        self.date_entry.pack(side=tk.LEFT)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
    def fill_headache(self):
        """Quick fill for headache"""
        self.clear_all()
        self.name_entry.insert(0, "Sample Patient")
        self.phn_entry.insert(0, "9876543210")
        self.phone_entry.insert(0, "(250) 555-0123")
        
        self.conditions['headache'].set(True)
        
        self.symptoms_text.insert(1.0, "Patient presents with bilateral tension-type headache, "
                                      "duration 2 days. No red flags. Pain 6/10.")
        self.medical_history_text.insert(1.0, "No significant PMHx. No drug allergies. No contraindications.")
        self.diagnosis_entry.insert(0, "Tension headache")
        self.medication_text.insert(1.0, "Acetaminophen 500mg PO q4-6h PRN #30 Refills: 0")
        
    def fill_uti(self):
        """Quick fill for UTI"""
        self.clear_all()
        self.name_entry.insert(0, "Sample Patient")
        self.phn_entry.insert(0, "9876543210")
        self.phone_entry.insert(0, "(250) 555-0123")
        
        self.conditions['uti'].set(True)
        
        self.symptoms_text.insert(1.0, "Dysuria, frequency, urgency x 2 days. "
                                      "No fever, flank pain, or vaginal symptoms.")
        self.medical_history_text.insert(1.0, "No recurrent UTIs. No drug allergies.")
        self.diagnosis_entry.insert(0, "Uncomplicated UTI")
        self.medication_text.insert(1.0, "Nitrofurantoin 100mg PO BID #10 Refills: 0")
        self.prescription_var.set(True)
        
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
        
    def save_json(self):
        """Save form data to JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "pre_checked": {
                "pharmacist_checked": True,
                "patient_eligible": True,
                "informed_consent": True
            },
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
            "prescription_issued": self.prescription_var.get(),
            "pharmacy": {
                "name": "Tablet Pharmacy 3",
                "address": "101-6373 Hammond Bay Rd, Nanaimo BC, V9S1Y1",
                "pharmacist": "Aki Shah",
                "license": "14901"
            },
            "follow_up": "Will be followed up in 5 days time",
            "date_signed": self.date_entry.get()
        }
        
        filename = f"macs_form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        # Show success message
        tk.messagebox.showinfo("Success", f"Form saved to {filename}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleMACSForm()
    app.run()