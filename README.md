# CSV Data Cleaner

A Python tool for validating and cleaning messy customer data from CSV files.

## Features

- ✅ Validates email addresses, ages, names, and cities
- 🔧 Automatically fixes common issues (whitespace, formatting)
- 📊 Generates detailed processing reports
- 📁 Separates clean data from unfixable errors

## Usage
```bash
python validator.py customers.csv
```

## What It Fixes

| Issue | Fix Applied |
|-------|-------------|
| `  JOHN@EMAIL.COM  ` | → `john@email.com` |
| `25.0` | → `25` |
| `  Bob Lee  ` | → `Bob Lee` |

## Output

- `customers_clean.csv` - Valid, cleaned records
- `customers_errors.csv` - Records that couldn't be fixed

## Example

**Input:**
```csv
name,email,age,city
  John Doe  ,JOHN@EMAIL.COM,25.0,NYC
Jane Smith,invalid.email,30,LA
```

**Output (clean):**
```csv
name,email,age,city
John Doe,john@email.com,25,NYC
```

**Output (errors):**
```csv
name,email,age,city
Jane Smith,invalid.email,30,LA
```



## Next Steps

- [ ] Add logging
- [ ] Support multiple file formats
- [ ] Add configuration file for validation rules
