@echo off
echo ============================================================
echo PDF Form Field Mapper V3 - Enhanced Drawing Interface
echo ============================================================
echo.
echo NEW FEATURES:
echo - Draw rectangles instead of clicking points
echo - Right-click any field to edit its name
echo - Numbered condition boxes with yellow borders
echo - Fixed font size of 10
echo.
echo FIELD MODE:
echo 1. Select field type (or Custom for your own name)
echo 2. Click and drag to draw a rectangle
echo 3. Right-click on any field to rename it
echo.
echo CONDITION MODE:
echo 1. Switch to Condition Boxes mode
echo 2. Draw yellow boxes around conditions
echo 3. Boxes are automatically numbered
echo 4. Tell Claude Desktop to select by number (e.g., "select conditions 2, 5, and 8")
echo.
echo Starting enhanced mapper...

"C:\Program Files\Python312\python.exe" form_field_mapper_v3.py

pause