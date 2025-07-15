#!/usr/bin/env python3
"""
Test script to simulate form filling based on image data
This will help us understand the exact workflow
"""

import json
from enhanced_pdf_filler_v2 import fill_pdf_with_numbers

# Extract information from the image004.jpg
# I can see in the Kroll pharmacy system:
# Patient: Isenor, Kristofor
# Phone: (250) 937-1689
# Drug: Terbinafine HCl
# Directions: Apply to the affected area(s) topically (nails) twice a day
# Quantity: 30 (from Disp Qty)
# Refills: 0 (from Rem Qty)

# For nail fungus, we use Box 13 (Onychomycosis)

form_data = {
    "patient_name": "Isenor, Kristofor",
    "phn": "1234567890",  # Not visible in image, using placeholder
    "phone": "(250) 937-1689",
    "condition_numbers": [13],  # Box 13 for Onychomycosis (nail fungus)
    "symptoms": "Thickened, discolored toenails with brittle texture. Yellow-brown discoloration of nail plates. Possible nail plate separation from nail bed.",
    "medical_history": "No known drug allergies. No contraindications to topical antifungals. Previous treatments may have been attempted.",
    "diagnosis": "Onychomycosis (nail fungus)",
    "medication": "Terbinafine HCl topical. Apply to the affected area(s) topically (nails) twice a day. Quantity: 30. Refills: 0\n\nFor best results: File down thickened nails before application. Keep nails clean and dry. Apply medication to entire nail, cuticle, and skin around nail. Continue treatment for full duration even if nail appears improved. Complete cure may take 6-12 months as healthy nail grows. Wear breathable footwear and change socks daily. Disinfect nail tools after each use."
}

# Test the form filling
print("Testing form fill with extracted data...")
print(json.dumps(form_data, indent=2))
print("\n" + "="*50 + "\n")

# Call the function
result = fill_pdf_with_numbers(form_data)
print("Result:", result)