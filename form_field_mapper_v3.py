#!/usr/bin/env python3
"""
Enhanced Form Field Mapper V3
- Draw rectangles for fields instead of clicking
- Edit field names after creation
- Numbered condition boxes with yellow borders
- Font size fixed at 10
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import json
import os

class FormFieldMapperV3:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PharmaCare Form Field Mapper V3 - Enhanced")
        self.root.geometry("1600x900")
        
        # Variables
        self.pdf_path = None
        self.pdf_doc = None
        self.current_page = 0
        self.photo = None
        self.scale = 1.0
        self.fields = {}
        self.condition_boxes = []
        self.mode = "field"  # "field" or "condition"
        self.font_size = 10  # Fixed font size
        
        # Drawing state
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.temp_rect = None
        self.field_rectangles = {}  # Store canvas rectangles for editing
        self.condition_rectangles = {}  # Store condition rectangles
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface"""
        # Top frame for controls
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Mode selection
        mode_frame = tk.LabelFrame(control_frame, text="Mapping Mode", padx=10, pady=5)
        mode_frame.grid(row=0, column=0, padx=5, sticky="nw")
        
        self.mode_var = tk.StringVar(value="field")
        tk.Radiobutton(mode_frame, text="Field Mapping", variable=self.mode_var, 
                      value="field", command=self.switch_mode).pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="Condition Boxes", variable=self.mode_var, 
                      value="condition", command=self.switch_mode).pack(anchor=tk.W)
        
        # File controls
        file_frame = tk.LabelFrame(control_frame, text="PDF File", padx=10, pady=5)
        file_frame.grid(row=0, column=1, padx=5, sticky="nw")
        
        tk.Button(file_frame, text="Load PDF", command=self.load_pdf, 
                 bg="#4CAF50", fg="white", width=12).pack(pady=2)
        tk.Button(file_frame, text="Save Mapping", command=self.save_mapping, 
                 bg="#2196F3", fg="white", width=12).pack(pady=2)
        tk.Button(file_frame, text="Load Mapping", command=self.load_mapping, 
                 bg="#FF9800", fg="white", width=12).pack(pady=2)
        tk.Button(file_frame, text="Clear All", command=self.clear_all, 
                 bg="#f44336", fg="white", width=12).pack(pady=2)
        
        # Field type selection (for field mode)
        self.field_frame = tk.LabelFrame(control_frame, text="Field Type", padx=10, pady=5)
        self.field_frame.grid(row=0, column=2, padx=5, sticky="nw")
        
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
            ("Custom Field", "custom")
        ]
        
        for text, value in field_types:
            tk.Radiobutton(self.field_frame, text=text, variable=self.field_type, 
                          value=value).pack(anchor=tk.W)
        
        # Edit controls
        edit_frame = tk.LabelFrame(control_frame, text="Edit Tools", padx=10, pady=5)
        edit_frame.grid(row=0, column=3, padx=5, sticky="nw")
        
        tk.Label(edit_frame, text="Right-click on any\nfield to edit its name", 
                font=("Arial", 9, "italic")).pack(pady=5)
        tk.Label(edit_frame, text="Font size: 10", 
                font=("Arial", 9)).pack(pady=5)
        
        # Instructions
        instructions_frame = tk.LabelFrame(control_frame, text="Instructions", padx=10, pady=5)
        instructions_frame.grid(row=0, column=4, padx=5, sticky="nw")
        
        instructions = """Field Mode:
1. Select field type
2. Click and drag to draw box
3. Right-click to edit name

Condition Mode:
1. Click and drag to create
   numbered yellow boxes
2. Boxes are auto-numbered
3. Tell Claude to select by number"""
        
        tk.Label(instructions_frame, text=instructions, justify=tk.LEFT, 
                font=("Arial", 9)).pack()
        
        # Status bar
        self.status_var = tk.StringVar(value="Load a PDF to begin mapping")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main canvas frame
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
                               xscrollcommand=h_scrollbar.set,
                               highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        # Enable mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Button-3>", self.on_right_click)  # Right-click
        
    def switch_mode(self):
        """Switch between field and condition mapping modes"""
        self.mode = self.mode_var.get()
        if self.mode == "field":
            self.status_var.set("Field mapping mode - draw rectangles for form fields")
        else:
            self.status_var.set("Condition mode - draw numbered yellow boxes for conditions")
        self.redraw_all()
    
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
        import io
        img = Image.open(io.BytesIO(img_data))
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(img)
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Display image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Update scroll region to include the entire image
        self.canvas.config(scrollregion=(0, 0, self.photo.width(), self.photo.height()))
        
        # Redraw all markers
        self.redraw_all()
    
    def on_mouse_down(self, event):
        """Start drawing rectangle"""
        if not self.pdf_doc:
            return
            
        self.drawing = True
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        
        # Delete temp rectangle if exists
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
    
    def on_mouse_drag(self, event):
        """Update rectangle while dragging"""
        if not self.drawing:
            return
            
        # Delete previous temp rectangle
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
        
        # Get current position
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        
        # Draw temp rectangle
        if self.mode == "field":
            self.temp_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y,
                outline="red", width=2, dash=(5, 5)
            )
        else:  # condition mode
            self.temp_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y,
                outline="gold", width=3, dash=(5, 5)
            )
    
    def on_mouse_up(self, event):
        """Finish drawing rectangle"""
        if not self.drawing:
            return
            
        self.drawing = False
        
        # Get final position
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        
        # Ensure we have a valid rectangle
        if abs(end_x - self.start_x) < 10 or abs(end_y - self.start_y) < 10:
            if self.temp_rect:
                self.canvas.delete(self.temp_rect)
            return
        
        # Convert to PDF coordinates
        x1 = min(self.start_x, end_x) / self.scale
        y1 = min(self.start_y, end_y) / self.scale
        x2 = max(self.start_x, end_x) / self.scale
        y2 = max(self.start_y, end_y) / self.scale
        
        if self.mode == "field":
            self.add_field_box(x1, y1, x2, y2)
        else:
            self.add_condition_box(x1, y1, x2, y2)
        
        # Delete temp rectangle
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
            self.temp_rect = None
        
        # Redraw
        self.redraw_all()
    
    def add_field_box(self, x1, y1, x2, y2):
        """Add a field box"""
        field_type = self.field_type.get()
        
        # If custom field, ask for name
        if field_type == "custom":
            field_name = simpledialog.askstring("Custom Field", "Enter field name:")
            if not field_name:
                return
            field_type = field_name
        
        # Add to fields
        if field_type not in self.fields:
            self.fields[field_type] = []
        
        self.fields[field_type].append({
            'page': self.current_page,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2
        })
        
        self.status_var.set(f"Added field: {field_type}")
    
    def add_condition_box(self, x1, y1, x2, y2):
        """Add a numbered condition box"""
        # Auto-number the box
        box_number = len(self.condition_boxes) + 1
        
        self.condition_boxes.append({
            'number': box_number,
            'page': self.current_page,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2
        })
        
        self.status_var.set(f"Added condition box #{box_number}")
    
    def redraw_all(self):
        """Redraw all field and condition markers"""
        # Clear existing markers (except the PDF image)
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if "field" in tags or "condition" in tags or "temp" in tags:
                self.canvas.delete(item)
        
        # Clear tracking dictionaries
        self.field_rectangles.clear()
        self.condition_rectangles.clear()
        
        # Draw field boxes
        if self.mode == "field":
            for field_type, boxes in self.fields.items():
                for i, box in enumerate(boxes):
                    if box['page'] == self.current_page:
                        self.draw_field_box(field_type, box, i)
        
        # Draw condition boxes
        for cond_box in self.condition_boxes:
            if cond_box['page'] == self.current_page:
                self.draw_condition_box(cond_box)
    
    def draw_field_box(self, field_type, box, index):
        """Draw a single field box"""
        x1 = box['x1'] * self.scale
        y1 = box['y1'] * self.scale
        x2 = box['x2'] * self.scale
        y2 = box['y2'] * self.scale
        
        # Draw rectangle
        rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="red", width=2,
            tags=("field", f"field_{field_type}_{index}")
        )
        
        # Draw label
        text_id = self.canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            text=field_type,
            fill="red", font=("Arial", self.font_size, "bold"),
            tags=("field", f"field_{field_type}_{index}")
        )
        
        # Store reference for editing
        key = f"{field_type}_{index}"
        self.field_rectangles[key] = {
            'rect_id': rect_id,
            'text_id': text_id,
            'field_type': field_type,
            'index': index
        }
    
    def draw_condition_box(self, cond_box):
        """Draw a single condition box"""
        x1 = cond_box['x1'] * self.scale
        y1 = cond_box['y1'] * self.scale
        x2 = cond_box['x2'] * self.scale
        y2 = cond_box['y2'] * self.scale
        
        # Draw yellow-bordered rectangle
        rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="gold", width=3,
            tags=("condition", f"condition_{cond_box['number']}")
        )
        
        # Draw number in corner
        num_id = self.canvas.create_text(
            x1 + 15, y1 + 15,
            text=str(cond_box['number']),
            fill="gold", font=("Arial", 14, "bold"),
            tags=("condition", f"condition_{cond_box['number']}")
        )
        
        # Add background for number visibility
        bbox = self.canvas.bbox(num_id)
        if bbox:
            bg_id = self.canvas.create_rectangle(
                bbox[0]-3, bbox[1]-3, bbox[2]+3, bbox[3]+3,
                fill="black", outline="",
                tags=("condition", f"condition_{cond_box['number']}")
            )
            self.canvas.tag_lower(bg_id, num_id)
        
        # Store reference
        self.condition_rectangles[cond_box['number']] = {
            'rect_id': rect_id,
            'num_id': num_id,
            'data': cond_box
        }
    
    def on_right_click(self, event):
        """Handle right-click for editing"""
        if self.mode != "field":
            return
            
        # Find clicked item
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        # Check if it's a field
        for tag in tags:
            if tag.startswith("field_") and "_" in tag[6:]:
                parts = tag[6:].split("_", 1)
                if len(parts) >= 2:
                    field_type = parts[0]
                    try:
                        index = int(parts[1])
                        self.edit_field_name(field_type, index)
                        break
                    except ValueError:
                        continue
    
    def edit_field_name(self, old_field_type, index):
        """Edit field name"""
        # Get new name
        new_name = simpledialog.askstring(
            "Edit Field Name", 
            f"Enter new name for '{old_field_type}':",
            initialvalue=old_field_type
        )
        
        if new_name and new_name != old_field_type:
            # Update field data
            if old_field_type in self.fields and index < len(self.fields[old_field_type]):
                box_data = self.fields[old_field_type].pop(index)
                
                # Remove old field type if empty
                if not self.fields[old_field_type]:
                    del self.fields[old_field_type]
                
                # Add to new field type
                if new_name not in self.fields:
                    self.fields[new_name] = []
                self.fields[new_name].append(box_data)
                
                # Redraw
                self.redraw_all()
                self.status_var.set(f"Renamed '{old_field_type}' to '{new_name}'")
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling (vertical)"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_shift_mousewheel(self, event):
        """Handle shift+mouse wheel scrolling (horizontal)"""
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def clear_all(self):
        """Clear all mappings"""
        if messagebox.askyesno("Clear All", "Remove all field and condition mappings?"):
            self.fields.clear()
            self.condition_boxes.clear()
            self.redraw_all()
            self.status_var.set("Cleared all mappings")
    
    def save_mapping(self):
        """Save field and condition mapping"""
        if not self.pdf_path:
            messagebox.showwarning("No PDF", "Please load a PDF first")
            return
            
        mapping_data = {
            'pdf_file': os.path.basename(self.pdf_path),
            'fields': self.fields,
            'condition_boxes': self.condition_boxes,
            'font_size': self.font_size,
            'context': 'PharmaCare MACS form with numbered condition boxes'
        }
        
        file_path = filedialog.asksaveasfilename(
            title="Save Mapping",
            defaultextension=".json",
            initialfile="macs_form_mapping_v3.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(mapping_data, f, indent=2)
            messagebox.showinfo("Success", f"Mapping saved to {file_path}")
            self.status_var.set(f"Saved: {os.path.basename(file_path)}")
    
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
                self.condition_boxes = mapping_data.get('condition_boxes', [])
                self.font_size = mapping_data.get('font_size', 10)
                
                # Try to load the PDF
                pdf_name = mapping_data.get('pdf_file', '')
                if pdf_name:
                    # Try different paths
                    possible_paths = [
                        os.path.join(os.path.dirname(file_path), pdf_name),
                        os.path.join(os.path.dirname(__file__), pdf_name)
                    ]
                    
                    for pdf_path in possible_paths:
                        if os.path.exists(pdf_path):
                            self.pdf_path = pdf_path
                            self.pdf_doc = fitz.open(pdf_path)
                            self.current_page = 0
                            self.display_page()
                            break
                    else:
                        # If PDF not found, just show a message
                        messagebox.showinfo("PDF Not Found", f"Could not find '{pdf_name}'. Please load the PDF manually.")
                
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load mapping: {str(e)}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FormFieldMapperV3()
    app.run()