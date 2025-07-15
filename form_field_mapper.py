#!/usr/bin/env python3
"""
Visual Form Field Mapper
Click on PDF to add numbered boxes and create a mapping for Claude Desktop
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import json
import os

class FormFieldMapper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Form Field Mapper")
        self.root.geometry("1200x800")
        
        self.pdf_path = None
        self.pdf_doc = None
        self.current_page = 0
        self.fields = []  # List of field definitions
        self.field_counter = 1
        self.current_image = None
        self.canvas_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the UI layout"""
        # Top toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Load PDF", command=self.load_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save Mapping", command=self.save_mapping).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Load Mapping", command=self.load_mapping).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Main area
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left: PDF display
        pdf_frame = ttk.LabelFrame(main_frame, text="PDF Preview (Click to add fields)")
        pdf_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Canvas for PDF
        self.canvas = tk.Canvas(pdf_frame, bg='gray', cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Right: Field list
        field_frame = ttk.LabelFrame(main_frame, text="Field Mappings")
        field_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        
        # Field type selector
        ttk.Label(field_frame, text="Field Type:").pack(anchor=tk.W, padx=5, pady=2)
        self.field_type = ttk.Combobox(field_frame, values=[
            "patient_name",
            "phn",
            "phone",
            "symptoms",
            "medical_history",
            "diagnosis",
            "medication",
            "date",
            "checkbox_pharmacist",
            "checkbox_eligible", 
            "checkbox_consent",
            "checkbox_acne",
            "checkbox_allergic_rhinitis",
            "checkbox_headache",
            "checkbox_uti",
            "checkbox_dermatitis",
            "checkbox_fungal_infection",
            "checkbox_herpes_labialis",
            "checkbox_impetigo",
            "checkbox_prescription",
            "custom"
        ], width=30)
        self.field_type.pack(padx=5, pady=2)
        self.field_type.set("patient_name")
        
        # Field list
        list_frame = ttk.Frame(field_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.field_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=40)
        self.field_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.field_listbox.yview)
        
        # Delete button
        ttk.Button(field_frame, text="Delete Selected", 
                  command=self.delete_selected).pack(pady=5)
        
        # Instructions
        instructions = """
Instructions:
1. Load your PDF
2. Click on the PDF where you want fields
3. Select field type before clicking
4. Save mapping when done

The mapping will be used by Claude Desktop
to know where to place each piece of data.
        """
        ttk.Label(field_frame, text=instructions, wraplength=300).pack(pady=10)
        
    def load_pdf(self):
        """Load a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.pdf_path = file_path
            self.pdf_doc = fitz.open(file_path)
            self.current_page = 0
            self.display_page()
            
    def display_page(self):
        """Display current PDF page"""
        if not self.pdf_doc:
            return
            
        # Get page
        page = self.pdf_doc[self.current_page]
        
        # Convert to image
        mat = fitz.Matrix(2, 2)  # 2x zoom for clarity
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("ppm")
        
        # Convert to PIL Image then to PhotoImage
        import io
        img = Image.open(io.BytesIO(img_data))
        
        # Resize to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        self.current_image = img
        self.photo = ImageTk.PhotoImage(img)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Redraw existing fields
        self.redraw_fields()
        
    def on_canvas_click(self, event):
        """Handle canvas click to add field"""
        if not self.current_image:
            return
            
        # Get click position relative to image
        x, y = event.x, event.y
        
        # Add field
        field = {
            'number': self.field_counter,
            'type': self.field_type.get(),
            'x': x,
            'y': y,
            'page': self.current_page
        }
        
        self.fields.append(field)
        self.field_counter += 1
        
        # Draw field marker
        self.draw_field(field)
        
        # Update list
        self.update_field_list()
        
    def draw_field(self, field):
        """Draw a field marker on canvas"""
        x, y = field['x'], field['y']
        num = field['number']
        
        # Draw rectangle
        rect = self.canvas.create_rectangle(
            x, y, x+100, y+20,
            outline='red', width=2
        )
        
        # Draw number
        text = self.canvas.create_text(
            x+50, y+10,
            text=f"#{num}",
            fill='red',
            font=('Arial', 10, 'bold')
        )
        
        # Store references
        field['rect'] = rect
        field['text'] = text
        
    def redraw_fields(self):
        """Redraw all fields on current page"""
        for field in self.fields:
            if field['page'] == self.current_page:
                self.draw_field(field)
                
    def update_field_list(self):
        """Update the field list display"""
        self.field_listbox.delete(0, tk.END)
        
        for field in sorted(self.fields, key=lambda f: f['number']):
            text = f"#{field['number']}: {field['type']} (x:{field['x']}, y:{field['y']})"
            self.field_listbox.insert(tk.END, text)
            
    def delete_selected(self):
        """Delete selected field"""
        selection = self.field_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.fields):
                # Remove from canvas
                field = self.fields[index]
                if 'rect' in field:
                    self.canvas.delete(field['rect'])
                if 'text' in field:
                    self.canvas.delete(field['text'])
                    
                # Remove from list
                self.fields.pop(index)
                self.update_field_list()
                
    def clear_all(self):
        """Clear all fields"""
        self.fields = []
        self.field_counter = 1
        self.canvas.delete("all")
        if self.canvas_image:
            self.canvas.itemconfig(self.canvas_image, image=self.photo)
        self.update_field_list()
        
    def save_mapping(self):
        """Save field mapping to JSON"""
        if not self.fields:
            messagebox.showwarning("No Fields", "No fields to save")
            return
            
        # Create mapping
        mapping = {
            'pdf_file': os.path.basename(self.pdf_path) if self.pdf_path else 'blank.pdf',
            'fields': {}
        }
        
        # Convert fields to mapping
        for field in self.fields:
            field_type = field['type']
            if field_type not in mapping['fields']:
                mapping['fields'][field_type] = []
                
            mapping['fields'][field_type].append({
                'number': field['number'],
                'x': field['x'],
                'y': field['y'],
                'page': field['page']
            })
            
        # Add metadata for Claude Desktop
        mapping['context'] = """
This is a PharmaCare MACS form mapping. When filling this form:
- Pharmacist Checked, Patient Eligible, and Informed Consent are always checked
- Only check condition boxes that match the patient's condition
- Date should be today's date
- Follow-up is always "5 days"
- Provider notification section remains empty
        """
        
        # Save file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="macs_form_mapping.json"
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(mapping, f, indent=2)
            messagebox.showinfo("Success", f"Mapping saved to {file_path}")
            
    def load_mapping(self):
        """Load field mapping from JSON"""
        file_path = filedialog.askopenfilename(
            title="Select Mapping File",
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            with open(file_path, 'r') as f:
                mapping = json.load(f)
                
            # Clear existing
            self.clear_all()
            
            # Load fields
            for field_type, positions in mapping['fields'].items():
                for pos in positions:
                    field = {
                        'number': pos['number'],
                        'type': field_type,
                        'x': pos['x'],
                        'y': pos['y'],
                        'page': pos.get('page', 0)
                    }
                    self.fields.append(field)
                    
            # Update counter
            if self.fields:
                self.field_counter = max(f['number'] for f in self.fields) + 1
                
            # Redraw
            self.redraw_fields()
            self.update_field_list()
            
            messagebox.showinfo("Success", "Mapping loaded")
            
    def run(self):
        # Update canvas size after window is shown
        self.root.after(100, self.display_page)
        self.root.mainloop()

if __name__ == "__main__":
    app = FormFieldMapper()
    app.run()