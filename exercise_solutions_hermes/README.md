# Exercise Solutions - Hermes Agent

This folder contains solutions for the local model exercises using Python scripts.

## 📁 Folder Structure

```
exercise_solutions_hermes/
└── data_scavenger/          # Level 1: Data Scavenger Exercises
    ├── ex01_name_email_company.py     # Exercise 1: Extract Name, Email, Company
    └── ex01_name_email_company.csv    # Output file with extracted data
```

## ✅ Completed Exercises

### Exercise 1: Clean Copy-Paste (Data Scavenger)
- **Input:** `exercise_data/L1_data/ex1_messy_profile.txt`
- **Task:** Extract Name, Email, and Company into separate columns
- **Output:** `ex01_name_email_company.csv`
- **Solution File:** `ex01_name_email_company.py`

### Results:
| Column | Value |
|--------|-------|
| Name | Alex Rivera |
| Email | alex.rivera@techflow.io |
| Company | TechFlow |

## 🚀 How to Run

```bash
cd exercise_solutions_hermes/data_scavenger
python3 ex01_name_email_company.py
```

## 📝 Notes

- All solutions use Python standard library (re, csv modules)
- No external dependencies required for Exercise 1
- Solutions are designed to be educational and easily modifiable
