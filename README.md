# PharmaCare MACS Form Filler

Automated PDF form filling system for PharmaCare MACS forms with Claude Desktop integration.

## Features
- Fill PharmaCare MACS forms automatically
- Condition box highlighting with red checkmarks
- Automatic text wrapping for symptoms and medication fields
- JSON-RPC integration with Claude Desktop

## Files
- `enhanced_pdf_filler_v2.py` - Core PDF filling logic with text wrapping
- `json_rpc_server.py` - JSON-RPC server for Claude Desktop
- `form_field_mapper_v3.py` - Visual tool for mapping form fields
- `macs_form_mapping_v3.json` - Field coordinates and mappings
- `blank.pdf` - Blank PharmaCare MACS form template
- `CONDITION_BOX_REFERENCE.txt` - Reference for condition numbers
- `PHARMACARE_FORM_INSTRUCTIONS.txt` - Detailed usage instructions

## Setup

1. Install required packages:
```bash
pip install PyMuPDF
```

2. Start the JSON-RPC server:
```bash
python json_rpc_server.py
```
Or use the batch file: `start_json_rpc_server.bat`

3. Configure Claude Desktop to use the server at `http://localhost:8080`

## Usage

The JSON-RPC server accepts the `fillPharmaCareForm` method with parameters:
- `patient_name` - Patient's full name (Last, First format)
- `phn` - Personal Health Number
- `phone` - Phone number
- `condition_numbers` - Array of condition box numbers to check
- `symptoms` - Patient symptoms (auto-wraps)
- `diagnosis` - Diagnosis information
- `medication` - Medication details (auto-wraps)

## Output
Filled forms are saved to: `C:\forms\[PatientFirstName]\[PatientFullName]_[timestamp].pdf`

## Condition Box Reference
See `CONDITION_BOX_REFERENCE.txt` for the complete list of condition numbers and their meanings.