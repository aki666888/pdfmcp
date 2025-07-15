# PharmaCare MACS Form - Condition Selection System

## Overview
The enhanced PharmaCare form filler now supports intelligent condition selection and highlighting. When Claude Desktop specifies conditions, the system will:

1. **Find the exact text** for each condition on the PDF
2. **Highlight the text** with a yellow background
3. **Mark the checkbox** with a red filled circle

## How It Works

### For Claude Desktop
When filling the form, Claude Desktop can specify conditions in the `conditions` array:

```json
{
  "patient_name": "John Doe",
  "phn": "1234567890",
  "phone": "(250) 555-1234",
  "conditions": ["tinea_pedis", "headache"],
  "symptoms": "Itchy feet, frequent headaches",
  "diagnosis": "Athlete's foot and tension headaches",
  "medication": "Topical antifungal, acetaminophen"
}
```

### Available Condition Codes
Claude Desktop should use these exact codes:

**Skin Conditions:**
- `acne` - Acne
- `dermatitis` - Dermatitis (general)
- `impetigo` - Impetigo
- `shingles` - Shingles
- `urticaria` - Urticaria, including insect bites

**Fungal Infections:**
- `tinea_pedis` - Tinea pedis (athlete's foot)
- `tinea_corporis` - Tinea corporis (ringworm)
- `tinea_cruris` - Tinea cruris (jock itch)
- `onychomycosis` - Onychomycosis (nail fungus)
- `vaginal_candidiasis` - Vaginal candidiasis
- `oropharyngeal_candidiasis` - Oropharyngeal candidiasis (thrush)

**Pain Conditions:**
- `headache` - Headache
- `dysmenorrhea` - Dysmenorrhea (menstrual pain)
- `musculoskeletal_pain` - Musculoskeletal pain

**Digestive:**
- `dyspepsia` - Dyspepsia (indigestion)
- `gastroesophageal_reflux` - GERD
- `oral_ulcers` - Oral ulcers

**Infections:**
- `conjunctivitis` - Conjunctivitis (pink eye)
- `herpes_labialis` - Herpes labialis (cold sores)
- `uti` - Urinary tract infection
- `threadworms` - Threadworms or pinworms

**Other:**
- `allergic_rhinitis` - Allergic rhinitis
- `hemorrhoids` - Hemorrhoids
- `nicotine_dependence` - Nicotine dependence
- `contraception` - Contraception

## Visual Indication Methods

The system uses two methods to indicate selected conditions:

1. **Text Highlighting** - The condition text is highlighted with a yellow background
2. **Checkbox Marking** - A red filled circle is drawn at the checkbox position

## MCP Server Commands

### Fill Form with Conditions
```
fill_pharmacare_form({
  "patient_name": "Jane Smith",
  "phn": "9876543210",
  "conditions": ["uti", "headache"],
  ...
})
```

### List All Conditions
```
list_conditions()
```

### Suggest Conditions Based on Symptoms
```
suggest_condition({
  "symptoms": "burning sensation during urination"
})
```

## Testing
Run `test_enhanced.py` to see examples of:
- Single condition selection
- Multiple condition selection
- Various condition types

## Form Field Mapper V2
The new `form_field_mapper_v2.py` supports:
- Traditional field mapping (text fields, checkboxes)
- Condition area mapping (draw rectangles around condition text)
- Both modes in one tool

This allows precise mapping of where conditions appear on the PDF for accurate highlighting.