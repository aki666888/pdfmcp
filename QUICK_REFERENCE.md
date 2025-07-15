# PharmaCare MACS Form - Quick Reference Card

## Essential Fields
```json
{
  "patient_name": "Last, First",
  "phone": "(250) 555-1234",
  "phn": "1234567890",
  "condition_numbers": [16],  // Box numbers
  "symptoms": "Patient symptoms",
  "medical_history": "Allergies, meds, contraindications",
  "diagnosis": "Clinical diagnosis",
  "medication": "Drug, sig, mitte, refills"
}
```

## Common Conditions Quick Lookup

### Infections
- **UTI**: Box 28
- **Athlete's foot**: Box 16
- **Vaginal yeast**: Box 30
- **Cold sores**: Box 21
- **Impetigo**: Box 22

### Skin Conditions
- **Acne**: Box 2
- **Contact dermatitis**: Box 6
- **Eczema (atopic)**: Box 7
- **Diaper rash**: Box 8
- **Hives**: Box 29
- **Shingles**: Box 26

### Pain
- **Headache**: Box 18
- **Period pain**: Box 10
- **Muscle/joint pain**: Box 25

### GI Issues
- **Heartburn/GERD**: Box 17
- **Indigestion**: Box 11

### Other
- **Allergies**: Box 3
- **Pink eye**: Box 4
- **Hemorrhoids**: Box 20
- **Contraception**: Box 1

## Medication Examples

### Topical Antifungals
"Clotrimazole 1% cream. Apply BID x 4 weeks. Mitte: 30g. Refills: 0"

### Antibiotics (UTI)
"Nitrofurantoin 100mg PO BID x 5 days. Mitte: 10. Refills: 0"

### Topical Steroids
"Hydrocortisone 1% cream. Apply BID x 7 days. Mitte: 15g. Refills: 0"

### Antihistamines
"Cetirizine 10mg PO daily PRN. Mitte: 30. Refills: 2"

## Quick Commands

List all conditions:
```
Use tool: list_condition_boxes
```

Fill complete form:
```
Use tool: fill_pharmacare_form
With the JSON data above
```

Quick fill presets:
```
Use tool: quick_fill_with_conditions
{
  "patient_name": "Name",
  "phn": "1234567890",
  "condition_preset": "skin" // or "infection", "pain", "respiratory"
}
```