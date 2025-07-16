# Development Guidelines - IMPORTANT

## Vision Accessibility Notice
The maintainer has vision issues. Please follow these guidelines to ensure the codebase remains accessible and manageable.

## Core Principles

### 1. File Management - NO VERSIONING
- **REPLACE files, don't create new versions**
  - ❌ BAD: `pdf_filler_v2.py`, `pdf_filler_v3.py`, `pdf_filler_final.py`
  - ✅ GOOD: Always update `pdf_filler.py` in place
- **Delete old files immediately after replacing**
- **Keep only ONE version of each file**

### 2. Repository Cleanliness
- **Maintain minimal file count** - only essential files
- **No temporary or backup files**
- **No test files in main directory**
- **Use .gitignore properly**

### 3. Code Simplicity
- **Keep code focused on core functionality**
- **Avoid over-engineering or premature optimization**
- **If it works, don't complicate it**
- **Prefer simple, readable solutions over clever ones**

### 4. Update Process
When updating code:
1. **Read the existing file first**
2. **Make minimal necessary changes**
3. **Replace the file (don't create new version)**
4. **Test the core functionality**
5. **Commit with clear message**
6. **Delete any temporary files created**

### 5. Essential Files Only

#### General Form Filler (generalformmcp)
```
claude_config.json          # Claude Desktop config
json_rpc_server.py         # JSON-RPC server
pdf_filler.py              # Core PDF filling logic
pdf_mapper.py              # Visual field mapper
README.md                  # Documentation
run_pdf_mapper.bat         # Run mapper
start_json_rpc_server.bat  # Start server
.gitignore                 # Git ignore rules
blanks_and_json/           # PDF templates and mappings
logs/                      # Log files
```

#### PharmaCare Form (pdfmcp)
```
enhanced_pdf_filler_v2.py   # Core PDF filler
json_rpc_server.py         # JSON-RPC server
form_field_mapper_v3.py    # Field mapper
macs_form_mapping_v3.json  # Field mappings
blank.pdf                  # Form template
CONDITION_BOX_REFERENCE.txt # Condition reference
PHARMACARE_FORM_INSTRUCTIONS.txt # Instructions
README.md                  # Documentation
start_json_rpc_server.bat  # Start server
run_mapper_v3.bat          # Run mapper
```

### 6. Git Commit Guidelines
- **One clear purpose per commit**
- **Replace files, don't add versions**
- **Use descriptive commit messages**
- Example: "Fix text wrapping in PDF filler" NOT "Add new version of filler"

### 7. Testing Guidelines
- **Test core functionality after changes**
- **Don't leave test files in repository**
- **Verify file output locations are correct**

### 8. Common Pitfalls to Avoid
- Creating multiple versions of the same file
- Adding unnecessary features
- Making code more complex than needed
- Leaving temporary files in repo
- Creating nested folders unnecessarily
- Adding files "just in case"

### 9. When in Doubt
- **Simpler is better**
- **Less files is better**
- **Working code is better than perfect code**
- **Ask: "Does this add essential value?"**

## Remember
The goal is a clean, simple, working system that's easy to maintain. Every file should have a clear purpose, and there should be only ONE version of each file.

**ALWAYS REPLACE, NEVER VERSION**