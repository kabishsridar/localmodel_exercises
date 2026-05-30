"""
Exercise 5: Regex for Humans - Formula Architect

Task: Clean this column of phone numbers so they all follow the format (XXX) XXX-XXXX.

Input File: exercise_data/L1_data/ex5_messy_phones.csv
Output Format: CSV with standardized phone numbers in (XXX) XXX-XXXX format
"""

import re
import csv


def normalize_phone_number(phone):
    """Normalize any phone number format to (XXX) XXX-XXXX."""
    
    if not phone or not isinstance(phone, str):
        return None
    
    # Remove all non-digit characters except + and parentheses
    digits = re.sub(r'[^\d]', '', phone)
    
    # Handle different length cases
    if len(digits) == 10:
        # Standard 10-digit number
        area_code = digits[:3]
        prefix = digits[3:6]
        line_num = digits[6:]
        return f"({area_code}) {prefix}-{line_num}"
    
    elif len(digits) == 11 and digits.startswith('1'):
        # US number with country code (1-XXX-XXX-XXXX)
        area_code = digits[1:4]
        prefix = digits[4:7]
        line_num = digits[7:]
        return f"({area_code}) {prefix}-{line_num}"
    
    elif len(digits) > 10:
        # Assume first digit is country code, extract last 10
        area_code = digits[-10:-7]
        prefix = digits[-7:-4]
        line_num = digits[-4:]
        return f"({area_code}) {prefix}-{line_num}"
    
    else:
        # Invalid length - return None to mark as invalid
        return None


def detect_phone_format(phone):
    """Detect the original format of a phone number."""
    
    if not phone or not isinstance(phone, str):
        return "Unknown"
    
    formats = {
        'Plain Digits': r'^\d{10,}$',
        '(XXX) XXX-XXXX': r'^\(\d{3}\)\s*\d{3}-\d{4}$',
        '(XXX) XXX XXXX': r'^\(\d{3}\)\s*\d{3}\s*\d{4}$',
        'XXX.XXX.XXXX': r'^\d{3}\.\d{3}\.\d{4}$',
        '+1-XXX-XXX-XXXX': r'^\+1-\d{3}-\d{3}-\d{4}$',
        'XXX XXX XXXX': r'^\d{3}\s+\d{3}\s+\d{4}$',
        '(XXX)-XXX-XXXX': r'^\(\d{3}\)-\d{3}-\d{4}$',
        '+1 XXX XXX XXXX': r'^\+1\s*\d{3}\s*\d{3}\s*\d{4}$',
    }
    
    for format_name, pattern in formats.items():
        if re.match(pattern, phone.strip()):
            return format_name
    
    return "Unknown Format"


def load_csv_data(file_path):
    """Load CSV data."""
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None


def process_phone_numbers(rows):
    """Process all phone numbers and add normalized versions."""
    
    processed_rows = []
    
    for row in rows:
        original_phone = row.get('Raw Phone Numbers', '').strip()
        
        # Detect format
        detected_format = detect_phone_format(original_phone)
        
        # Normalize phone number
        normalized_phone = normalize_phone_number(original_phone)
        
        # Determine status
        if normalized_phone:
            status = "✅ Valid"
            confidence = "High"
        else:
            status = "❌ Invalid Format"
            confidence = "Low"
        
        processed_rows.append({
            'Original': original_phone,
            'Detected_Format': detected_format,
            'Normalized': normalized_phone if normalized_phone else '',
            'Status': status,
            'Confidence': confidence
        })
    
    return processed_rows


def display_results(processed_rows):
    """Display the cleaning results."""
    
    print("\n" + "="*100)
    print("REGEX FOR HUMANS - Phone Number Standardization")
    print("="*100)
    print("\n📋 FORMATTING RULE APPLIED:")
    print("   All phone numbers converted to: (XXX) XXX-XXXX format")
    print("   Handles formats like: 1234567890, (987) 654-3210, 555.123.4567, +1-212-555-0199")
    print("="*100 + "\n")
    
    # Print header
    print(f"{'Original':<20} | {'Detected Format':<25} | {'Normalized (XXX) XXX-XXXX':<20} | {'Status':<15}")
    print("-" * 100)
    
    for row in processed_rows:
        original = row['Original'][:18] + ".." if len(row['Original']) > 20 else row['Original']
        detected = row['Detected_Format'][:23] + ".." if len(row['Detected_Format']) > 25 else row['Detected_Format']
        
        normalized = row['Normalized'][:18] + ".." if len(row['Normalized']) > 20 else row['Normalized']
        
        status = f"{row['Status']} ({row['Confidence']})"
        
        print(f"{original:<20} | {detected:<25} | {normalized:<20} | {status:<15}")
    
    print("\n" + "="*100)


def calculate_statistics(processed_rows):
    """Calculate cleaning statistics."""
    
    valid_count = sum(1 for row in processed_rows if row['Status'] == '✅ Valid')
    invalid_count = len(processed_rows) - valid_count
    
    # Count by detected format
    format_counts = {}
    for row in processed_rows:
        fmt = row['Detected_Format']
        format_counts[fmt] = format_counts.get(fmt, 0) + 1
    
    print("\n" + "="*80)
    print("CLEANING STATISTICS")
    print("="*80)
    
    print(f"\n📊 Processing Summary:")
    print(f"   ✅ Successfully Normalized: {valid_count} phone numbers ({(valid_count/len(processed_rows)*100):.1f}%)")
    print(f"   ❌ Invalid Format:          {invalid_count} phone number(s) ({(invalid_count/len(processed_rows)*100):.1f}%)")
    
    print(f"\n📋 Original Formats Detected:")
    for fmt, count in sorted(format_counts.items(), key=lambda x: -x[1]):
        bar = "█" * min(count * 5, 40)
        print(f"   {fmt:<30} | {bar} ({count})")
    
    print("\n" + "="*80)


def save_to_csv(processed_rows, output_file):
    """Save the cleaned data to CSV."""
    
    try:
        fieldnames = ['Original', 'Detected_Format', 'Normalized', 'Status', 'Confidence']
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in processed_rows:
                writer.writerow(row)
        
        print(f"✅ Successfully saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def generate_excel_regex():
    """Generate Excel formulas and regex patterns for users."""
    
    print("\n" + "="*80)
    print("EXCEL FORMULAS & REGEX PATTERNS")
    print("="*80)
    
    print("\n📝 Excel Formula to Normalize Phone Numbers:")
    print("""   =LET(
       phone, A2,
       digits, SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(phone, "-", ""), ".", ""), "(", ""),
       digits, SUBSTITUTE(digits, ")", ""),
       IF(LEN(digits)=10, "("&LEFT(digits,3)&") "&MID(digits,4,3)&"-"&RIGHT(digits,4),
          IF(LEN(digits)=11, "("&MID(digits,2,3)&") "&MID(digits,5,3)&"-"&RIGHT(digits,4), "Invalid"))
   )""")
    
    print("\n📝 Regular Expression Pattern for Validation:")
    print("   ^\\(\\d{3}\\) \\d{3}-\\d{4}$")
    print("   (Matches: (XXX) XXX-XXXX format)")
    
    print("\n📝 Python Regex to Extract Digits from Any Format:")
    print("""   import re
   digits = re.sub(r'[^\\d]', '', phone_number)""")
    
    print("\n" + "="*80)


def main():
    """Main function to run the Regex for Humans exercise."""
    
    # Define file paths
    input_file = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_data/L1_data/ex5_messy_phones.csv"
    output_csv = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_solutions_hermes/formula_architecture/ex05_regex_for_humans.csv"
    
    print("="*100)
    print("EXERCISE 5: FORMULA ARCHITECT - Regex for Humans")
    print("="*100 + "\n")
    
    # Load data
    rows = load_csv_data(input_file)
    
    if rows:
        # Process phone numbers
        processed_rows = process_phone_numbers(rows)
        
        # Display results
        display_results(processed_rows)
        
        # Calculate statistics
        calculate_statistics(processed_rows)
        
        # Generate Excel formulas for reference
        generate_excel_regex()
        
        # Save to CSV
        save_to_csv(processed_rows, output_csv)
        
        print("\n🎉 Exercise completed successfully!")
    else:
        print("❌ Failed to load data.")


if __name__ == "__main__":
    main()
