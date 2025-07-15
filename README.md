# PharmaCare MACS Form Filler

Automated PDF form filling system for PharmaCare MACS forms using Claude Desktop and OpenRPC.

## Quick Setup (Windows + Claude Desktop)

### 1. Install Prerequisites
- Python 3.12 or higher
- Node.js (for OpenRPC)
- Claude Desktop

### 2. Clone Repository
```bash
git clone https://github.com/aki666888/pdfmcp.git
cd pdfmcp
```

### 3. Configure Claude Desktop
Add to `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "openrpc": {
      "command": "npx",
      "args": ["-y", "@open-rpc/server-js"],
      "env": {}
    }
  }
}
```

### 4. Start JSON-RPC Server
Double-click `start_json_rpc_server.bat` or run:
```bash
"C:\Program Files\Python312\python.exe" json_rpc_server.py
```

### 5. Restart Claude Desktop
Completely quit and restart Claude Desktop.

## Usage in Claude Desktop

Use the RPC tool to fill forms:
```
Use RPC to call fillPharmaCareForm at http://localhost:8080 with:
{
  "patient_name": "Smith, John",
  "phn": "9876543210", 
  "phone": "(250) 555-1234",
  "condition_numbers": [16],
  "symptoms": "Athlete's foot with itching and redness",
  "diagnosis": "Tinea pedis",
  "medication": "Clotrimazole 1% cream, apply twice daily"
}
```

## Condition Box Numbers
1. Contraception
2. Acne
3. Allergic rhinitis
4. Conjunctivitis
5-9. Various Dermatitis types
10. Dysmenorrhea
11. Dyspepsia
12-16. Fungal infections
17. GERD
18. Headache
19. Hemorrhoids
20. Herpes labialis
21-23. Infections
24. Insect bites
25. Intertrigo
26. Musculoskeletal pain
27. Nausea/Vomiting
28. Oral thrush
29. Pinworms
30. UTI

## Files
- `enhanced_pdf_filler_v2.py` - PDF filling logic with symptoms fix
- `form_field_mapper_v3.py` - GUI tool for mapping fields
- `json_rpc_server.py` - JSON-RPC server (port 8080)
- `blank.pdf` - Template PDF form
- `macs_form_mapping_v3.json` - Field mappings

## Creating/Editing Mappings
Run `run_mapper_v3.bat` to open the mapping tool.

## Architecture
```
Claude Desktop → OpenRPC → JSON-RPC Server (8080) → PDF Filler
```