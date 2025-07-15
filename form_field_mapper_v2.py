#!/usr/bin/env python3
"""
Enhanced Form Field Mapper V2
Supports both field mapping and condition area mapping
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import json
import os

class FormFieldMapperV2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PharmaCare Form Field Mapper V2")
        self.root.geometry("1400x900")
        
        # Variables
        self.pdf_path = None
        self.pdf_doc = None
        self.current_page = 0
        self.photo = None
        self.scale = 1.0
        self.fields = {}
        self.condition_areas = []
        self.field_counter = 1
        self.mode = "field"  # "field" or "condition"
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface"""
        # Top frame for controls
        control_frame = tk.Frame(self.root, bg="#f0f0f0", height=100)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Mode selection
        mode_frame = tk.LabelFrame(control_frame, text="Mapping Mode", padx=10, pady=5)
        mode_frame.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="field")
        tk.Radiobutton(mode_frame, text="Field Mapping", variable=self.mode_var, 
                      value="field", command=self.switch_mode).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Condition Areas", variable=self.mode_var, 
                      value="condition", command=self.switch_mode).pack(side=tk.LEFT)
        
        # File controls
        file_frame = tk.LabelFrame(control_frame, text="PDF File", padx=10, pady=5)
        file_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Button(file_frame, text="Load PDF", command=self.load_pdf, 
                 bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Save Mapping", command=self.save_mapping, 
                 bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Load Mapping", command=self.load_mapping, 
                 bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Field type selection (for field mode)
        self.field_frame = tk.LabelFrame(control_frame, text="Field Type", padx=10, pady=5)
        self.field_frame.pack(side=tk.LEFT, padx=5)
        
        self.field_type = tk.StringVar(value="patient_name")
        field_types = [
            ("Patient Name", "patient_name"),
            ("PHN", "phn"),
            ("Phone", "phone"),
            ("Date", "date"),
            ("Symptoms", "symptoms"),
            ("Medical History", "medical_history"),
            ("Diagnosis", "diagnosis"),
            ("Medication", "medication"),
            ("Pharmacist Checked", "checkbox_pharmacist"),
            ("Patient Eligible", "checkbox_eligible"),
            ("Informed Consent", "checkbox_consent"),
            ("Prescription", "checkbox_prescription")
        ]
        
        for text, value in field_types:
            tk.Radiobutton(self.field_frame, text=text, variable=self.field_type, 
                          value=value).pack(anchor=tk.W)
        
        # Condition selection (for condition mode)
        self.condition_frame = tk.LabelFrame(control_frame, text="Condition Selection", padx=10, pady=5)
        # Initially hidden
        
        condition_list = [
            "Contraception", "Acne", "Allergic rhinitis", "Conjunctivitis",
            "Dermatitis", "Dysmenorrhea", "Dyspepsia", "Fungal infections",
            "Headache", "Hemorrhoids", "Herpes labialis", "Impetigo",
            "Nicotine dependence", "Oral ulcers", "Oropharyngeal candidiasis",
            "Musculoskeletal pain", "Shingles", "Threadworms", "UTI",
            "Urticaria", "Vaginal candidiasis", "Tinea pedis", "Tinea corporis",
            "Tinea cruris", "Onychomycosis", "Gastroesophageal reflux"
        ]
        
        self.condition_listbox = tk.Listbox(self.condition_frame, selectmode=tk.MULTIPLE, height=10)
        for condition in condition_list:
            self.condition_listbox.insert(tk.END, condition)
        self.condition_listbox.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(self.condition_frame, text="Mark Selected Areas", 
                 command=self.mark_condition_areas, bg="#9C27B0", fg="white").pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Load a PDF to begin mapping")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main canvas
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg="gray", 
                               yscrollcommand=v_scrollbar.set,
                               xscrollcommand=h_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Instructions
        instructions = """
        Field Mapping Mode:
        1. Load your PDF
        2. Select field type
        3. Click where you want the field
        4. Save your mapping
        
        Condition Mode:
        1. Switch to Condition Areas mode
        2. Select conditions from list
        3. Click "Mark Selected Areas"
        4. Draw rectangles around condition text
        """
        
        info_frame = tk.LabelFrame(self.root, text="Instructions", padx=10, pady=5)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        tk.Label(info_frame, text=instructions, justify=tk.LEFT, 
                wraplength=250).pack()
        
    def switch_mode(self):
        """Switch between field and condition mapping modes"""
        if self.mode_var.get() == "field":
            self.field_frame.pack(side=tk.LEFT, padx=5)
            self.condition_frame.pack_forget()
            self.mode = "field"
            self.status_var.set("Field mapping mode - click to add fields")
        else:
            self.field_frame.pack_forget()
            self.condition_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
            self.mode = "condition"
            self.status_var.set("Condition mapping mode - select conditions and mark areas")
    
    def load_pdf(self):
        """Load a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.pdf_path = file_path
                self.pdf_doc = fitz.open(file_path)
                self.current_page = 0
                self.display_page()
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")
    
    def display_page(self):
        """Display current page of PDF"""
        if not self.pdf_doc:
            return
            
        # Get page
        page = self.pdf_doc[self.current_page]
        
        # Render page to pixmap
        mat = fitz.Matrix(self.scale, self.scale)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img_data = pix.tobytes("ppm")
        img = Image.open(tk.io.BytesIO(img_data))
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(img)
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Display image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Update scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        # Redraw existing fields and condition areas
        self.redraw_markers()
    
    def redraw_markers(self):
        """Redraw all field markers and condition areas"""
        # Draw field markers
        for field_type, positions in self.fields.items():
            for pos in positions:
                if pos['page'] == self.current_page:
                    # Draw rectangle
                    x, y = pos['x'] * self.scale, pos['y'] * self.scale
                    self.canvas.create_rectangle(
                        x, y, x + 100, y + 20,
                        outline="red", width=2,
                        tags=("field", field_type)
                    )
                    # Draw label
                    self.canvas.create_text(
                        x + 50, y + 10,
                        text=f"{field_type}",
                        fill="red", font=("Arial", 8),
                        tags=("field", field_type)
                    )
        
        # Draw condition areas
        for area in self.condition_areas:
            if area['page'] == self.current_page:
                x1, y1 = area['x1'] * self.scale, area['y1'] * self.scale
                x2, y2 = area['x2'] * self.scale, area['y2'] * self.scale
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="purple", width=3,
                    tags=("condition", area['condition'])
                )
                # Draw condition name
                self.canvas.create_text(
                    (x1 + x2) / 2, y1 - 10,
                    text=area['condition'],
                    fill="purple", font=("Arial", 10, "bold"),
                    tags=("condition", area['condition'])
                )
    
    def on_canvas_click(self, event):
        """Handle canvas click"""
        if not self.pdf_doc:
            return
        
        if self.mode == "field":
            # Get click position relative to PDF
            canvas_x = self.canvas.canvasx(event.x)
            canvas_y = self.canvas.canvasy(event.y)
            
            # Convert to PDF coordinates
            pdf_x = canvas_x / self.scale
            pdf_y = canvas_y / self.scale
            
            # Get current field type
            field_type = self.field_type.get()
            
            # Add to fields
            if field_type not in self.fields:
                self.fields[field_type] = []
            
            self.fields[field_type].append({
                'page': self.current_page,
                'x': pdf_x,
                'y': pdf_y
            })
            
            # Redraw
            self.redraw_markers()
            
            # Update status
            self.status_var.set(f"Added {field_type} at ({int(pdf_x)}, {int(pdf_y)})")
    
    def mark_condition_areas(self):
        """Start marking areas for selected conditions"""
        selected_indices = self.condition_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select conditions to map")
            return
        
        selected_conditions = [self.condition_listbox.get(i) for i in selected_indices]
        
        # Create a dialog for drawing rectangles
        dialog = tk.Toplevel(self.root)
        dialog.title("Mark Condition Areas")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text=f"Draw rectangles around these conditions:\n{', '.join(selected_conditions)}", 
                wraplength=350).pack(pady=10)
        
        tk.Label(dialog, text="Click and drag on the PDF to draw rectangles", 
                font=("Arial", 10, "italic")).pack(pady=5)
        
        self.drawing_conditions = selected_conditions
        self.current_condition_index = 0
        self.rect_start = None
        self.temp_rect = None
        
        # Bind mouse events for rectangle drawing
        self.canvas.bind("<ButtonPress-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)
        
        tk.Button(dialog, text="Done", command=lambda: self.finish_condition_mapping(dialog),
                 bg="#4CAF50", fg="white").pack(pady=10)
        
        self.status_var.set(f"Draw rectangle for: {selected_conditions[0]}")
    
    def start_rect(self, event):
        """Start drawing rectangle"""
        self.rect_start = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
    
    def draw_rect(self, event):
        """Draw temporary rectangle"""
        if self.rect_start:
            if self.temp_rect:
                self.canvas.delete(self.temp_rect)
            x1, y1 = self.rect_start
            x2, y2 = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            self.temp_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="purple", width=2, dash=(5, 5)
            )
    
    def end_rect(self, event):
        """End drawing rectangle"""
        if self.rect_start and hasattr(self, 'drawing_conditions'):
            x1, y1 = self.rect_start
            x2, y2 = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            
            # Convert to PDF coordinates
            pdf_x1, pdf_y1 = x1 / self.scale, y1 / self.scale
            pdf_x2, pdf_y2 = x2 / self.scale, y2 / self.scale
            
            # Ensure proper ordering
            if pdf_x1 > pdf_x2:
                pdf_x1, pdf_x2 = pdf_x2, pdf_x1
            if pdf_y1 > pdf_y2:
                pdf_y1, pdf_y2 = pdf_y2, pdf_y1
            
            # Add condition area
            condition = self.drawing_conditions[self.current_condition_index]
            self.condition_areas.append({
                'condition': condition,
                'page': self.current_page,
                'x1': pdf_x1,
                'y1': pdf_y1,
                'x2': pdf_x2,
                'y2': pdf_y2
            })
            
            # Move to next condition
            self.current_condition_index += 1
            if self.current_condition_index < len(self.drawing_conditions):
                self.status_var.set(f"Draw rectangle for: {self.drawing_conditions[self.current_condition_index]}")
            else:
                self.status_var.set("Finished marking condition areas")
            
            # Cleanup
            if self.temp_rect:
                self.canvas.delete(self.temp_rect)
            self.rect_start = None
            
            # Redraw
            self.redraw_markers()
    
    def finish_condition_mapping(self, dialog):
        """Finish condition mapping"""
        # Unbind mouse events
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        
        # Re-bind click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        dialog.destroy()
        self.status_var.set("Condition mapping complete")
    
    def save_mapping(self):
        """Save field and condition mapping"""
        if not self.pdf_path:
            messagebox.showwarning("No PDF", "Please load a PDF first")
            return
            
        mapping_data = {
            'pdf_file': os.path.basename(self.pdf_path),
            'fields': self.fields,
            'condition_areas': self.condition_areas,
            'context': 'PharmaCare MACS form with condition mapping'
        }
        
        file_path = filedialog.asksaveasfilename(
            title="Save Mapping",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(mapping_data, f, indent=2)
            messagebox.showinfo("Success", f"Mapping saved to {file_path}")
            self.status_var.set(f"Saved mapping: {os.path.basename(file_path)}")
    
    def load_mapping(self):
        """Load existing mapping"""
        file_path = filedialog.askopenfilename(
            title="Load Mapping",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    mapping_data = json.load(f)
                
                self.fields = mapping_data.get('fields', {})
                self.condition_areas = mapping_data.get('condition_areas', [])
                
                # Try to load the PDF
                pdf_name = mapping_data.get('pdf_file', '')
                pdf_path = os.path.join(os.path.dirname(file_path), pdf_name)
                if os.path.exists(pdf_path):
                    self.pdf_path = pdf_path
                    self.pdf_doc = fitz.open(pdf_path)
                    self.current_page = 0
                    self.display_page()
                
                self.status_var.set(f"Loaded mapping: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load mapping: {str(e)}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FormFieldMapperV2()
    app.run()