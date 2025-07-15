#!/usr/bin/env python3
"""
Test script for enhanced PDF filling with condition selection
"""

from enhanced_pdf_filler import fill_enhanced_pdf

# Test case 1: Athlete's foot
print("Test 1: Athlete's foot patient")
result = fill_enhanced_pdf({
    "patient_name": "Sarah Johnson",
    "phn": "9876543210",
    "phone": "(250) 555-1234",
    "conditions": ["tinea_pedis"],  # Single condition
    "symptoms": "Itchy, scaly skin between toes",
    "medical_history": "No known allergies",
    "diagnosis": "Tinea pedis (athlete's foot)",
    "medication": "Topical clotrimazole 1% cream",
    "prescription_issued": True
})
print(result)
print("-" * 50)

# Test case 2: Multiple conditions
print("\nTest 2: Multiple conditions")
result = fill_enhanced_pdf({
    "patient_name": "Michael Chen",
    "phn": "1234567890",
    "phone": "(250) 555-5678",
    "conditions": ["headache", "dyspepsia"],  # Multiple conditions
    "symptoms": "Frequent tension headaches, indigestion after meals",
    "medical_history": "GERD",
    "diagnosis": "Tension headaches, dyspepsia",
    "medication": "Acetaminophen 500mg, Famotidine 20mg",
    "prescription_issued": False
})
print(result)
print("-" * 50)

# Test case 3: Skin condition with multiple types
print("\nTest 3: Dermatitis patient")
result = fill_enhanced_pdf({
    "patient_name": "Emily Davis",
    "phn": "5555555555",
    "phone": "(250) 555-9999",
    "conditions": ["dermatitis", "urticaria"],  # Related skin conditions
    "symptoms": "Red, itchy patches on arms, hives from insect bites",
    "medical_history": "Sensitive skin, seasonal allergies",
    "diagnosis": "Contact dermatitis, urticaria",
    "medication": "Hydrocortisone 1% cream, Cetirizine 10mg",
    "prescription_issued": True
})
print(result)
print("-" * 50)

# Test case 4: UTI
print("\nTest 4: UTI patient")
result = fill_enhanced_pdf({
    "patient_name": "Jennifer Wilson",
    "phn": "7777777777",
    "phone": "(250) 555-3333",
    "conditions": ["uti"],
    "symptoms": "Burning sensation during urination, frequency",
    "medical_history": "Previous UTI 6 months ago",
    "diagnosis": "Uncomplicated urinary tract infection",
    "medication": "Nitrofurantoin 100mg BID x 5 days",
    "prescription_issued": True
})
print(result)