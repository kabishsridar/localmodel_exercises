"""
Exercise 2: Browser-to-Sheet - Data Scavenger

Task: Read clipboard data (tab-separated) and format it as a clean Excel table with proper headers.

Input File: exercise_data/L1_data/ex2_clipboard_table.txt
Output Format: CSV file ready for Excel import + Formatted table view
"""

import re
import csv


def parse_clipboard_data(file_path):
    """Parse tab-separated clipboard data into structured format."""
    
    rows = []
    headers = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # First line contains headers (tab-separated)
        if lines:
            headers = [col.strip() for col in lines[0].strip().split('\t')]
            
            # Remaining lines contain data
            for i, line in enumerate(lines[1:], start=2):
                if line.strip():  # Skip empty lines
                    columns = [cell.strip() for cell in line.strip().split('\t')]
                    
                    # Create dictionary with headers as keys
                    row_dict = {}
                    for j, header in enumerate(headers):
                        if j < len(columns):
                            row_dict[header] = columns[j]
                        else:
                            row_dict[header] = ""  # Handle missing columns
                    
                    rows.append(row_dict)
                    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None, None
    
    return headers, rows


def clean_table_data(headers, rows):
    """Clean and standardize the data for better presentation."""
    
    cleaned_rows = []
    
    for row in rows:
        cleaned_row = {}
        
        # Clean Product ID (ensure SKU format)
        if 'Product ID' in row:
            product_id = row['Product ID']
            if not product_id.startswith('SKU-'):
                cleaned_row['Product ID'] = f"SKU-{product_id}"
            else:
                cleaned_row['Product ID'] = product_id
        
        # Clean Price (remove $, convert to float for calculations)
        if 'Price' in row:
            price_str = row['Price'].replace('$', '').strip()
            try:
                price_float = float(price_str)
                cleaned_row['Price'] = f"${price_float:.2f}"  # Format back to currency
                cleaned_row['Price_Float'] = price_float  # Keep numeric version
            except ValueError:
                cleaned_row['Price'] = row['Price']
                cleaned_row['Price_Float'] = 0.0
        
        # Clean Stock (ensure it's a number)
        if 'Stock' in row:
            try:
                stock_val = int(row['Stock'])
                cleaned_row['Stock'] = str(stock_val)
                cleaned_row['Stock_Int'] = stock_val  # Keep numeric version
                
                # Add low stock indicator for items with < 10 units
                if stock_val < 10:
                    cleaned_row['⚠️ Low Stock?'] = 'YES'
                else:
                    cleaned_row['⚠️ Low Stock?'] = 'NO'
                    
            except ValueError:
                cleaned_row['Stock'] = row['Stock']
                cleaned_row['Stock_Int'] = 0
        
        # Keep other fields as-is (Category, Last Restock)
        for key in ['Category', 'Last Restock']:
            if key in row:
                cleaned_row[key] = row[key]
        
        cleaned_rows.append(cleaned_row)
    
    return cleaned_rows


def display_table(headers, rows):
    """Display the data as a formatted table."""
    
    print("\n" + "="*80)
    print("CLEAN EXCEL TABLE - FORMATTED OUTPUT")
    print("="*80)
    
    # Print headers with proper alignment
    max_widths = {}
    for header in headers:
        max_widths[header] = len(header)
    
    for row in rows:
        for key, value in row.items():
            if key.endswith('_Float') or key.endswith('_Int'):
                continue  # Skip numeric versions from display
            width = max(len(str(value)), max_widths.get(key, len(key)))
            max_widths[key] = min(width + 2, 25)  # Cap at 27 chars
    
    print("\n" + "|".join([f"{h:<{max_widths[h]}}" for h in headers if not h.endswith('_Float') and not h.endswith('_Int')]))
    print("-" * sum(max_widths.values()))
    
    for row in rows:
        display_row = []
        for key in headers:
            if not key.endswith('_Float') and not key.endswith('_Int'):
                value = row.get(key, '')
                # Add low stock indicator
                if key == 'Stock' and row.get('Stock_Int', 0) < 10:
                    display_row.append(f"⚠️ {value:<{max_widths[key]-2}}")
                else:
                    display_row.append(f"{str(value):<{max_widths[key]}}")
        print("|".join(display_row))
    
    print("\n" + "="*80)


def save_to_csv(headers, rows, output_file):
    """Save the cleaned data to CSV file ready for Excel."""
    
    try:
        with open(output_file, 'w', newline='') as csvfile:
            if not headers:
                return False
            
            fieldnames = [h for h in headers if not h.endswith('_Float') and not h.endswith('_Int')] + ['⚠️ Low Stock?']
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in rows:
                write_row = {}
                for key in fieldnames:
                    if key in row:
                        write_row[key] = row[key]
                    elif key == '⚠️ Low Stock?':
                        write_row[key] = 'YES' if row.get('Stock_Int', 0) < 10 else 'NO'
                writer.writerow(write_row)
        
        print(f"✅ Successfully saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def generate_excel_ready_data(headers, rows):
    """Generate additional summary statistics for Excel."""
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS FOR EXCEL")
    print("="*80)
    
    # Calculate total inventory value
    total_value = sum(row.get('Price_Float', 0) * row.get('Stock_Int', 0) for row in rows)
    
    # Count low stock items
    low_stock_count = sum(1 for row in rows if row.get('Stock_Int', 0) < 10)
    
    # Category breakdown
    category_counts = {}
    for row in rows:
        cat = row.get('Category', 'Unknown')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print(f"\n📊 Total Inventory Value: ${total_value:.2f}")
    print(f"⚠️ Items with Low Stock (<10): {low_stock_count}")
    print(f"\n📁 Category Breakdown:")
    for cat, count in category_counts.items():
        print(f"   - {cat}: {count} items")
    
    print("="*80 + "\n")


def main():
    """Main function to run the Browser-to-Sheet exercise."""
    
    # Define file paths
    input_file = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_data/L1_data/ex2_clipboard_table.txt"
    output_csv = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_solutions_hermes/data_scavenger/ex02_browser_to_sheet.csv"
    
    print("="*80)
    print("EXERCISE 2: DATA SCAVENGER - Browser-to-Sheet")
    print("="*80 + "\n")
    
    # Parse clipboard data
    headers, rows = parse_clipboard_data(input_file)
    
    if headers and rows:
        # Clean the data
        cleaned_rows = clean_table_data(headers, rows)
        
        # Display formatted table
        display_table(headers, cleaned_rows)
        
        # Generate summary statistics
        generate_excel_ready_data(headers, cleaned_rows)
        
        # Save to CSV (Excel-ready format)
        save_to_csv(headers, cleaned_rows, output_csv)
        
        print("🎉 Exercise completed successfully!")
    else:
        print("❌ Failed to parse clipboard data.")


if __name__ == "__main__":
    main()
