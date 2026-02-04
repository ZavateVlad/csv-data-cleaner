# CSV Data Cleaner

A Python tool for validating and cleaning messy customer data from CSV files.

## Features

- Validates email addresses, ages, names, and cities
- Automatically fixes common issues (whitespace, formatting)
- Generates detailed processing reports
- Separates clean data from unfixable errors

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

## What I Learned

Building this project helped me understand:

- **File I/O**: Reading/writing CSV files with context managers (`with open()`)
- **String manipulation**: Using `.strip()`, `.lower()`, `.title()` for data cleaning
- **Regex**: Email validation patterns with `re.match()`
- **Error handling**: Try-except blocks for robust validation
- **Data structures**: Converting CSV rows to dictionaries with `zip()`
- **Command-line arguments**: Using `sys.argv` for flexible inputs
