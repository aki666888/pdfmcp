# PharmaCare MACS Form - Claude Desktop Instructions

## Overview
This MCP server allows you to fill PharmaCare Minor Ailments and Contraception Service (MACS) forms automatically. The form will be saved as a PDF in the patient's folder.

## Available Tools

### 1. `fill_pharmacare_form`
Main tool for filling the complete form with all patient information.

### 2. `list_condition_boxes`
Lists all numbered condition boxes and what conditions they represent.

### 3. `quick_fill_with_conditions`
Quick fill with preset condition groups (skin, infection, pain, respiratory).

## Form Fields Guide

### Patient Information Section
- **patient_name**: Full patient name (e.g., "Smith, John" or "Jane Doe")
- **phone**: Patient phone number (e.g., "(250) 555-1234")
- **phn**: Personal Health Number - 10 digits (e.g., "9876543210")

### Medical Information
- **symptoms**: Patient's symptoms and signs (text box)
  - Example: "Itchy, red patches on feet with scaling between toes"
  
- **medical_history**: Assessment of relevant medical history and medications
  - Include: Current medications, allergies, contraindications
  - Example: "No known drug allergies. Currently taking metformin for diabetes."

- **diagnosis**: Clinical diagnosis
  - Example: "Tinea pedis (athlete's foot)"

### Recommendations Section
- **medication**: Complete medication details including:
  - Medication name, strength, sig, mitte, refills
  - Example: "Clotrimazole 1% cream. Apply BID to affected areas x 4 weeks. Mitte: 30g. Refills: 0"

### Pre-filled Information
The following are automatically filled:
- ✓ Pharmacist Checked
- ✓ Patient Eligible  
- ✓ Informed Consent: Yes
- Date: Today's date
- Pharmacy information: Aki Shah, Tablet Pharmacy 3

## Condition Selection

### Using Numbered Boxes
Conditions are selected by specifying box numbers in the `condition_numbers` array:

| Box # | Condition |
|-------|-----------|
| 1 | Contraception |
| 2 | Acne |
| 3 | Allergic rhinitis |
| 4 | Conjunctivitis |
| 6 | Dermatitis - allergic/contact |
| 7 | Dermatitis - atopic |
| 8 | Dermatitis - diaper rash |
| 9 | Dermatitis - seborrheic |
| 10 | Dysmenorrhea |
| 11 | Dyspepsia |
| 12 | Fungal infections |
| 13 | Onychomycosis |
| 14 | Tinea corporis |
| 15 | Tinea cruris |
| 16 | Tinea pedis |
| 17 | Gastroesophageal reflux |
| 18 | Headache |
| 19 | Nicotine dependence |
| 20 | Hemorrhoids |
| 21 | Herpes labialis |
| 22 | Impetigo |
| 23 | Oral ulcers |
| 24 | Oropharyngeal candidiasis |
| 25 | Musculoskeletal pain |
| 26 | Shingles |
| 27 | Threadworms/pinworms |
| 28 | Urinary tract infection |
| 29 | Urticaria/insect bites |
| 30 | Vaginal candidiasis |

## Example Usage

### Example 1: Athlete's Foot
```json
{
  "patient_name": "Johnson, Sarah",
  "phone": "(250) 555-1234",
  "phn": "9876543210",
  "condition_numbers": [16],
  "symptoms": "Itchy, scaly skin between toes. Red, peeling skin on soles of feet. Burning sensation.",
  "medical_history": "No known allergies. No current medications. No contraindications to topical antifungals.",
  "diagnosis": "Tinea pedis (athlete's foot)",
  "medication": "Clotrimazole 1% cream. Apply BID to affected areas x 4 weeks. Mitte: 30g. Refills: 0"
}
```

### Example 2: UTI
```json
{
  "patient_name": "Chen, Michael",
  "phone": "(250) 555-5678",
  "phn": "1234567890",
  "condition_numbers": [28],
  "symptoms": "Dysuria, urinary frequency and urgency x 2 days. No fever or flank pain.",
  "medical_history": "NKDA. No current medications. Previous UTI 6 months ago - resolved with antibiotics.",
  "diagnosis": "Uncomplicated urinary tract infection",
  "medication": "Nitrofurantoin 100mg PO BID x 5 days. Mitte: 10 tablets. Refills: 0"
}
```

### Example 3: Multiple Conditions
```json
{
  "patient_name": "Davis, Emily",
  "phone": "(250) 555-9999",
  "phn": "5555555555",
  "condition_numbers": [2, 6],
  "symptoms": "Facial acne with comedones and papules. Red, itchy rash on hands after using new soap.",
  "medical_history": "Sensitive skin. Uses moisturizer daily. No oral medications.",
  "diagnosis": "Acne vulgaris; Contact dermatitis",
  "medication": "1) Benzoyl peroxide 5% gel daily to face. 2) Hydrocortisone 1% cream BID to hands x 7 days"
}
```

### Example 4: Quick Fill
For common conditions, use the quick fill tool:
```json
{
  "patient_name": "Wilson, James",
  "phn": "7777777777",
  "condition_preset": "skin"
}
```
This will select boxes: 2, 6, 7, 22, 26, 29 (skin conditions)

## Prescription Options
- If prescribing: Set prescription details in medication field
- If advising OTC only: Leave prescription section unchecked

## Output
Forms are saved to: `C:/forms/[PatientFirstName]/`
- PDF file: `MACS_Form_[Name]_[Timestamp].pdf`
- JSON data: `MACS_Form_[Name]_[Timestamp].json`

## Tips
1. Always include complete medication instructions (sig, mitte, refills)
2. Be specific with symptoms to justify the diagnosis
3. Document any relevant medical history or contraindications
4. Multiple conditions can be selected by providing multiple box numbers
5. Use the `list_condition_boxes` tool if you need to see all available conditions

## Common Condition Groups
- **Dermatitis**: Use boxes 6-9 for specific types
- **Fungal infections**: Box 12 (general) or 13-16 for specific types
- **Women's health**: Boxes 1 (contraception), 10 (dysmenorrhea), 30 (vaginal candidiasis)
- **GI issues**: Boxes 11 (dyspepsia), 17 (GERD)

## Error Prevention
- Ensure PHN is exactly 10 digits
- Include area code in phone numbers
- Be specific with medication dosing
- Select appropriate condition boxes for the diagnosis