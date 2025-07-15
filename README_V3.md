# PharmaCare MACS Form - Version 3 Enhanced Features

## New Features in V3

### 1. Drawing Interface
- **Draw rectangles** instead of clicking points
- Click and drag to create field boxes
- More intuitive and precise field placement

### 2. Editable Field Names
- **Right-click** any field to edit its name
- Create custom fields with any name you want
- Select "Custom Field" option and enter your own name

### 3. Numbered Condition Boxes
- Yellow-bordered boxes for conditions
- Automatically numbered (1, 2, 3, etc.)
- Claude Desktop selects by number instead of condition name

### 4. Fixed Font Size
- All text is rendered at font size 10
- Consistent appearance across all fields

## How to Use

### Step 1: Run the Mapper
```batch
run_mapper_v3.bat
```

### Step 2: Map Your Form

#### Field Mapping Mode:
1. Load your PDF
2. Select field type (or Custom)
3. Click and drag to draw rectangle
4. Right-click to rename any field

#### Condition Mode:
1. Switch to "Condition Boxes" mode
2. Draw rectangles around each condition
3. Boxes are automatically numbered
4. Save your mapping

### Step 3: Use with Claude Desktop

Instead of specifying condition names, Claude Desktop now uses numbers:

```json
{
  "patient_name": "John Doe",
  "phn": "1234567890",
  "condition_numbers": [2, 5, 8],
  "symptoms": "Patient symptoms",
  "diagnosis": "Clinical diagnosis"
}
```

## Example Condition Mapping

If you've drawn boxes around conditions in this order:
1. Contraception
2. Acne
3. Allergic rhinitis
4. Conjunctivitis
5. Dermatitis
...and so on

Claude Desktop would specify `"condition_numbers": [2]` to select Acne.

## Benefits

1. **More Flexible** - Draw boxes of any size
2. **Easier to Edit** - Right-click to rename fields
3. **Clearer for LLM** - Numbers are unambiguous
4. **Visual Feedback** - Yellow borders make conditions obvious

## Files

- `form_field_mapper_v3.py` - Enhanced mapping tool
- `enhanced_pdf_filler_v2.py` - PDF filler using numbered boxes
- `mcp_server_numbered.py` - MCP server for numbered conditions
- `run_mapper_v3.bat` - Easy launcher for the mapper

## MCP Configuration

Update your Claude Desktop config to use the numbered server:

```json
"pharmacare-form": {
  "command": "C:\\Program Files\\Python312\\python.exe",
  "args": ["C:\\mcp-servers\\pharmacare-form\\mcp_server_numbered.py"],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```