# PharmaCare MACS Form Filler

An automated PDF form filler for PharmaCare MACS forms, designed to work with Claude Desktop through MCP (Model Context Protocol).

## Features

- Automatically fills patient information, conditions, and prescriptions
- Works with static PDF forms using overlay approach
- Numbered condition boxes for easy selection
- Text wrapping for long medication and symptom descriptions
- Integration with Claude Desktop via OpenRPC MCP server

## Requirements

- Python 3.12+
- PyMuPDF (fitz)
- MCP SDK

## Installation

1. Clone this repository:
```bash
git clone https://github.com/aki666888/pdfmcp.git
cd pdfmcp
```

2. Install required Python packages:
```bash
pip install PyMuPDF mcp
```

3. Configure Claude Desktop:
Add the following to your `claude_desktop_config.json`:

```json
"pharmacare-form": {
  "command": "C:\\Program Files\\Python312\\python.exe",
  "args": ["C:\\mcp-servers\\pharmacare-form\\simple_mcp_server.py"],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
},
"openrpc": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-openrpc", "http://localhost:8080"]
}
```

## Usage

1. Start the JSON-RPC server:
```bash
python json_rpc_server.py
```
Or use the batch file:
```bash
start_json_rpc_server.bat
```

2. In Claude Desktop, upload a prescription image and specify the condition

3. The form will be automatically filled and saved to `C:/forms/`

## File Structure

- `enhanced_pdf_filler_v2.py` - Core PDF filling logic with numbered condition boxes
- `form_field_mapper_v3.py` - GUI tool for mapping form fields
- `json_rpc_server.py` - JSON-RPC server for OpenRPC integration
- `simple_mcp_server.py` - MCP server for Claude Desktop
- `macs_form_mapping_v3_updated.json` - Field mappings for the PDF form

## Condition Box Numbers

- Box 1: Contraception
- Box 2: Acne
- Box 3: Allergic rhinitis
- Box 4: Conjunctivitis
- Box 6: Dermatitis - allergic/contact
- Box 7: Dermatitis - atopic
- Box 8: Dermatitis - diaper rash
- Box 9: Dermatitis - seborrheic
- Box 10: Dysmenorrhea
- Box 11: Dyspepsia
- Box 12: Fungal infections
- Box 13: Onychomycosis
- Box 14: Tinea corporis infection
- Box 15: Tinea cruris infection
- Box 16: Tinea pedis infection
- Box 17: Gastroesophageal reflux disease
- Box 18: Headache
- Box 19: Nicotine dependence
- Box 20: Hemorrhoids
- Box 21: Herpes labialis
- Box 22: Impetigo
- Box 23: Oral ulcers
- Box 24: Oropharyngeal candidiasis
- Box 25: Musculoskeletal pain
- Box 26: Shingles
- Box 27: Threadworms or pinworms
- Box 28: Urinary tract infection
- Box 29: Urticaria, including insect bites
- Box 30: Vaginal candidiasis

## Output Format

Forms are saved as: `{FirstName}_{YYYYMMDD}_{HHMMSS}.pdf` in `C:/forms/`