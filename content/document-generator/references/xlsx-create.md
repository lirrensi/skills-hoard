# XLSX Creation & Editing

## Quick Start

### Read Data
```python
import pandas as pd

df = pd.read_excel('file.xlsx')
df = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets
```

### Create with Formulas
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
sheet = wb.active

sheet['A1'] = 'Header'
sheet['B1'] = '=SUM(A2:A10)'  # Use formulas, NOT hardcoded values

sheet['A1'].font = Font(bold=True)
sheet['A1'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

wb.save('output.xlsx')
```

### Edit Existing
```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb.active

sheet['A1'] = 'New Value'
wb.save('modified.xlsx')
```

## Critical Rules

⚠️ **Always use formulas, NOT hardcoded calculated values:**
```python
# ✅ CORRECT
sheet['B2'] = '=SUM(A1:A10)'

# ❌ WRONG
sheet['B2'] = 500  # Hardcoded
```

### Financial Model Standards
- **Blue text**: Hardcoded inputs
- **Black text**: Formulas
- **Green text**: Links to other sheets
- **Red text**: External links
- **Yellow background**: Key assumptions

### Number Formatting
- Years: Text ("2024" not "2,024")
- Currency: `$#,##0;($#,##0);-` (shows "-" for zeros)
- Percentages: `0.0%`
- Negatives: Use parentheses `(123)`

## Recalculation (Required)

After creating/editing with formulas:
```bash
python scripts/recalc.py output.xlsx
```

Check for errors:
- `#REF!` - Invalid reference
- `#DIV/0!` - Division by zero
- `#VALUE!` - Wrong data type
- `#NAME?` - Unrecognized function

## Best Practices

- Use `data_only=True` to read calculated values (but don't save with this)
- Specify dtypes: `pd.read_excel('file.xlsx', dtype={'id': str})`
- Use openpyxl for formatting, pandas for data analysis
- Document sources for hardcoded values
