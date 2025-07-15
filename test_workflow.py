#!/usr/bin/env python3
"""
Test workflow for understanding the form filling process
Based on image004.jpg (nail fungus prescription)
"""

import json
from datetime import datetime

# Simulate the workflow that Claude Desktop should follow

print("=== PHARMACARE FORM FILLING WORKFLOW ===\n")

# Step 1: Extract from image
print("STEP 1: Extracting information from image004.jpg")
print("-" * 40)
extracted_data = {
    "patient_name": "Isenor, Kristofor",
    "phone": "(250) 937-1689",
    "drug_name": "Terbinafine HCl",
    "directions": "Apply to the affected area(s) topically (nails) twice a day",
    "disp_qty": "30",
    "rem_qty": "0"
}
print("Extracted from Kroll system:")
for key, value in extracted_data.items():
    print(f"  {key}: {value}")

# Step 2: Map condition to box number
print("\nSTEP 2: Mapping condition to box number")
print("-" * 40)
print("User said: 'nail fungus'")
print("Mapping: nail fungus → Onychomycosis → Box 13")
condition_box = 13

# Step 3: Generate clinical information
print("\nSTEP 3: Generating clinical information")
print("-" * 40)
clinical_info = {
    "symptoms": "Thickened, discolored toenails with brittle texture. Yellow-brown discoloration of nail plates. Possible nail plate separation from nail bed.",
    "medical_history": "No known drug allergies. No contraindications to topical antifungals.",
    "diagnosis": "Onychomycosis (nail fungus)"
}
for key, value in clinical_info.items():
    print(f"{key}:")
    print(f"  {value}")

# Step 4: Format medication properly
print("\nSTEP 4: Formatting medication information")
print("-" * 40)
medication = f"{extracted_data['drug_name']} topical. {extracted_data['directions']}. Quantity: {extracted_data['disp_qty']}. Refills: {extracted_data['rem_qty']}"
print("Formatted medication:")
print(f"  {medication}")

additional_info = """
For best results: File down thickened nails before application. Keep nails clean and dry. Apply medication to entire nail, cuticle, and skin around nail. Continue treatment for full duration even if nail appears improved. Complete cure may take 6-12 months as healthy nail grows. Wear breathable footwear and change socks daily. Disinfect nail tools after each use."""

# Step 5: Create final JSON for MCP
print("\nSTEP 5: Creating JSON for fill_pharmacare_form")
print("-" * 40)
final_json = {
    "patient_name": extracted_data["patient_name"],
    "phn": "1234567890",  # Would need to be extracted or provided
    "phone": extracted_data["phone"],
    "condition_numbers": [condition_box],
    "symptoms": clinical_info["symptoms"],
    "medical_history": clinical_info["medical_history"],
    "diagnosis": clinical_info["diagnosis"],
    "medication": medication + additional_info
}

print("Final JSON to send to MCP server:")
print(json.dumps(final_json, indent=2))

# Step 6: Expected output
print("\nSTEP 6: Expected output")
print("-" * 40)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
print(f"PDF will be saved to: C:/forms/Kristofor/MACS_Form_Kristofor_{timestamp}.pdf")
print(f"JSON will be saved to: C:/forms/Kristofor/MACS_Form_Kristofor_{timestamp}.json")
print("Condition box 13 (Onychomycosis) will be highlighted")

# Summary for Claude Desktop
print("\n=== SUMMARY FOR CLAUDE DESKTOP ===")
print("-" * 40)
print("""
When user uploads an image and says "this is for nail fungus":

1. Extract visible data from image (name, phone, drug details)
2. Map "nail fungus" → Box 13 (Onychomycosis)
3. Generate appropriate symptoms for nail fungus
4. Format medication EXACTLY as shown: drug, directions, quantity, refills
5. Add helpful usage instructions after the medication
6. Call fill_pharmacare_form with the complete JSON
""")