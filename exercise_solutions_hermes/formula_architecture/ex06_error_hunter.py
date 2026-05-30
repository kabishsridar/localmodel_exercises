"""
Exercise 6: Error Hunter - Formula Architect

Task: Identify why these formulas are breaking and fix them.

Input File: exercise_data/L1_data/ex6_broken_formulas.csv
Output Format: CSV with fixed Total calculations and diagnostic information
"""

import csv


def detect_error_type(value):
    """Detect the type of error in a value."""
    
    if not value or value.strip() == '':
        return "Empty/Blank"
    
    value_upper = value.strip().upper()
    
    if value_upper == '#VALUE!':
        return "#VALUE! - Formula Error (invalid calculation)"
    elif value_upper == '#DIV/0!':
        return "#DIV/0! - Division by Zero"
    elif value_upper == '#N/A':
        return "#N/A - Value Not Available"
    elif value_upper == '#REF!':
        return "#REF! - Invalid Cell Reference"
    elif value_upper == 'NA' or value_upper == 'N/A':
        return "Text: N/A (Not Applicable)"
    elif value_upper == 'ERROR':
        return "Text: ERROR (Invalid data entry)"
    elif value.replace('.', '').replace('-', '').isdigit():
        return "Valid Number"
    elif value.strip().startswith('$'):
        return "Currency Format"
    else:
        return "Non-numeric Text (may cause calculation errors)"


def fix_total_calculation(quantity, unit_price):
    """Calculate the correct total given quantity and unit price."""
    
    try:
        # Try to parse quantity as number
        if not quantity or quantity.strip() == '':
            return None, "Empty Quantity"
        
        qty_value = float(quantity)
        
        # Check for non-numeric values that look like text
        if isinstance(quantity, str):
            if quantity.strip().lower() in ['none', 'null', 'n/a', 'unknown']:
                return None, "Text Value: None/Null"
        
        # Try to parse unit price as number
        if not unit_price or unit_price.strip() == '' or unit_price.upper() == 'N/A' or unit_price.upper() == 'ERROR':
            return None, f"Invalid Price: {unit_price}"
        
        price_value = float(unit_price.replace('$', '').strip())
        
        # Calculate total
        total = qty_value * price_value
        
        if total >= 1000:
            status = "✅ Valid & Significant Amount"
        else:
            status = "✅ Valid Amount"
        
        return round(total, 2), status
        
    except ValueError as e:
        return None, f"Parse Error: {str(e)}"
    except Exception as e:
        return None, f"Unknown Error: {str(e)}"


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


def analyze_and_fix_rows(rows):
    """Analyze each row for errors and fix calculations."""
    
    analyzed_rows = []
    
    error_categories = {
        'Quantity Issues': 0,
        'Price Issues': 0,
        'Formula Errors': 0,
        'Valid Data': 0
    }
    
    for idx, row in enumerate(rows, start=2):  # Start at 2 (row numbers)
        item = row.get('Item', '')
        quantity = row.get('Quantity', '')
        unit_price = row.get('Unit Price', '')
        original_total = row.get('Total', '')
        
        # Detect errors in input fields
        qty_error_type = detect_error_type(quantity)
        price_error_type = detect_error_type(unit_price)
        total_error_type = detect_error_type(original_total)
        
        # Try to fix the calculation
        fixed_total, calc_status = fix_total_calculation(quantity, unit_price)
        
        # Determine overall error category
        if qty_error_type.startswith('Non-numeric Text') or 'Text Value' in qty_error_type:
            error_category = "Quantity Issues"
            error_category_id = 1
            error_categories['Quantity Issues'] += 1
        elif price_error_type in ['Text: N/A (Not Applicable)', 'Text: ERROR (Invalid data entry)']:
            error_category = "Price Issues"
            error_category_id = 2
            error_categories['Price Issues'] += 1
        elif total_error_type.startswith('#VALUE!') or total_error_type.startswith('#DIV/0!'):
            error_category = "Formula Errors"
            error_category_id = 3
            error_categories['Formula Errors'] += 1
        else:
            error_category = "Valid Data"
            error_category_id = 4
            error_categories['Valid Data'] += 1
        
        # Determine if original total was correct
        is_original_correct = False
        correction_made = None
        
        if fixed_total is not None and original_total != '#VALUE!':
            try:
                if abs(float(original_total) - fixed_total) < 0.01:
                    is_original_correct = True
                    correction_made = "No change needed"
                else:
                    is_original_correct = False
                    correction_made = f"Corrected from ${float(original_total):.2f}" if original_total != '#VALUE!' else "Calculated new value"
            except ValueError:
                correction_made = "Calculated new value (original was error)"
        elif fixed_total is not None:
            correction_made = "Fixed broken formula"
        
        analyzed_rows.append({
            'Row': idx,
            'Item': item,
            'Quantity': quantity,
            'Qty_Issue': qty_error_type,
            'Unit_Price': unit_price,
            'Price_Issue': price_error_type,
            'Original_Total': original_total,
            'Total_Error': total_error_type,
            'Fixed_Total': f"${fixed_total:,.2f}" if fixed_total else "N/A",
            'Calculation_Status': calc_status,
            'Correction_Made': correction_made,
            'Error_Category': error_category,
            'Recommendation': generate_recommendation(error_category)
        })
    
    return analyzed_rows, error_categories


def generate_recommendation(category):
    """Generate recommendation based on error category."""
    
    recommendations = {
        'Quantity Issues': "Check for text values like 'None', 'N/A' in quantity field. Use IFERROR() wrapper.",
        'Price Issues': "Ensure all prices are numeric. Replace 'Error', 'N/A' with 0 or proper value.",
        'Formula Errors': "Recalculate using =IF(ISNUMBER(B2)*ISNUMBER(C2), B2*C2, 0). Handle blanks gracefully.",
        'Valid Data': "No action needed - data is correct."
    }
    
    return recommendations.get(category, "Review the data manually.")


def display_analysis(analyzed_rows):
    """Display the error analysis results."""
    
    print("\n" + "="*130)
    print("ERROR HUNTER - Formula Diagnostics & Fixes")
    print("="*130)
    print("\n📋 DIAGNOSTIC APPROACH:")
    print("   1. Identify why each formula is breaking")
    print("   2. Calculate correct totals where possible")
    print("   3. Provide recommendations for prevention")
    print("="*130 + "\n")
    
    # Print header
    print(f"{'Row':<5} | {'Item':<12} | {'Qty':<10} | {'Price':<10} | {'Orig Total':<12} | {'Fixed Total':<14} | {'Status'}")
    print("-" * 130)
    
    for row in analyzed_rows:
        item = row['Item'][:10] + ".." if len(row['Item']) > 12 else row['Item']
        qty = str(row['Quantity'])[:8] + ".." if len(str(row['Quantity'])) > 10 else row['Quantity']
        price = str(row['Unit_Price'])[:8] + ".." if len(str(row['Unit_Price'])) > 10 else row['Unit_Price']
        
        orig_total = str(row['Original_Total'])[:10] + ".." if len(str(row['Original_Total'])) > 12 else row['Original_Total']
        fixed_total = str(row['Fixed_Total'])[:12] + ".." if len(str(row['Fixed_Total'])) > 14 else row['Fixed_Total']
        
        status = f"{row['Calculation_Status'][:12]} ({row['Error_Category'][:8]})"
        
        print(f"{row['Row']:<5} | {item:<12} | {qty:<10} | {price:<10} | {orig_total:<12} | {fixed_total:<14} | {status}")
    
    print("\n" + "="*130)


def display_detailed_findings(analyzed_rows):
    """Display detailed findings for each problematic row."""
    
    print("\n" + "="*80)
    print("DETAILED FINDINGS & FIXES")
    print("="*80)
    
    for row in analyzed_rows:
        if row['Error_Category'] != 'Valid Data':
            print(f"\n🔍 Row {row['Row']} - {row['Item']}:")
            print(f"   Issue:     {row['Qty_Issue']} | {row['Price_Issue']}")
            print(f"   Original:  = {row['Original_Total']}")
            print(f"   Fixed:     = {row['Fixed_Total']}")
            print(f"   Action:    {row['Correction_Made']}")
            print(f"   💡 Recommendation: {row['Recommendation']}")
    
    print("\n" + "="*80)


def display_excel_formulas():
    """Display Excel formulas to prevent these errors."""
    
    print("\n" + "="*80)
    print("EXCEL FORMULAS TO PREVENT ERRORS")
    print("="*80)
    
    print("""
📝 Recommended Formula for Column D (Total):

=IF(AND(ISNUMBER(B2), ISNUMBER(C2)), B2*C2, 
   IF(B2="None" OR C2="Error", 0, 
      IFERROR(B2*C2, "Check Data")))

Or simpler robust version:
=IF(AND(NOT(ISBLANK(B2)), NOT(ISBLANK(C2))), B2*C2, 0)

For error highlighting (Conditional Formatting):
=OR(ISERROR(D2), ISNUMBER(FIND("Error", C2)))

""")
    
    print("="*80)


def display_summary(error_categories):
    """Display summary statistics."""
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    total_rows = sum(error_categories.values())
    
    for category, count in error_categories.items():
        percentage = (count / total_rows * 100) if total_rows > 0 else 0
        
        # Add emoji based on severity
        emojis = {
            'Valid Data': '✅',
            'Quantity Issues': '⚠️',
            'Price Issues': '⚠️',
            'Formula Errors': '❌'
        }
        
        print(f"   {emojis[category]} {category:<20} | {count:>3} rows ({percentage:5.1f}%)")
    
    # Calculate potential savings from fixes
    total_fixed_value = sum(
        float(row['Fixed_Total'].replace('$', '').replace(',', '')) 
        for row in analyzed_rows 
        if row['Fixed_Total'] != 'N/A'
    )
    
    print(f"\n💰 Total Value After Fixes: ${total_fixed_value:,.2f}")
    print("="*80)


def save_to_csv(analyzed_rows, output_file):
    """Save the analysis results to CSV."""
    
    try:
        fieldnames = [
            'Row', 'Item', 'Quantity', 'Qty_Issue', 
            'Unit_Price', 'Price_Issue', 'Original_Total', 
            'Total_Error', 'Fixed_Total', 'Calculation_Status',
            'Correction_Made', 'Error_Category', 'Recommendation'
        ]
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in analyzed_rows:
                writer.writerow(row)
        
        print(f"✅ Successfully saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


# Global variable for analyzed rows (needed by display_summary)
analyzed_rows = []


def main():
    """Main function to run the Error Hunter exercise."""
    
    global analyzed_rows
    
    # Define file paths
    input_file = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_data/L1_data/ex6_broken_formulas.csv"
    output_csv = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_solutions_hermes/formula_architecture/ex06_error_hunter.csv"
    
    print("="*130)
    print("EXERCISE 6: FORMULA ARCHITECT - Error Hunter")
    print("="*130 + "\n")
    
    # Load data
    rows = load_csv_data(input_file)
    
    if rows:
        # Analyze and fix
        analyzed_rows, error_categories = analyze_and_fix_rows(rows)
        
        # Display results
        display_analysis(analyzed_rows)
        display_detailed_findings(analyzed_rows)
        display_excel_formulas()
        display_summary(error_categories)
        
        # Save to CSV
        save_to_csv(analyzed_rows, output_csv)
        
        print("\n🎉 Exercise completed successfully!")
    else:
        print("❌ Failed to load data.")


if __name__ == "__main__":
    main()
