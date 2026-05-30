"""
Exercise 1: Clean Copy-Paste - Data Scavenger

Task: Extract the Name, Email, and Company into separate columns from messy text data.

Input File: exercise_data/L1_data/ex1_messy_profile.txt
Output Format: CSV with Name, Email, and Company columns
"""

import re
import csv


def parse_profile_data(file_path):
    """Parse messy profile text and extract structured data."""
    
    # Initialize variables to store extracted data
    name = ""
    email = ""
    company = ""
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Extract Name (Line starting with "Name:")
        name_match = re.search(r'Name:\s*(.+)', content)
        if name_match:
            name = name_match.group(1).strip()
        
        # Extract Email (pattern: xxx@xxx.xxx)
        email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        if email_matches:
            email = email_matches[0]
        
        # Extract Company (from "at [Company Name]" pattern or from email domain)
        company_match = re.search(r'at\s+([A-Za-z\s]+?)(?:\s|$)', content)
        if company_match:
            company = company_match.group(1).strip()
        
        # Fallback: Extract company from email domain if not found in text
        if not company and email:
            company = email.split('@')[1].split('.')[0].title() + " Solutions"
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None
    
    return {
        'Name': name,
        'Email': email,
        'Company': company
    }


def save_to_csv(data_dict, output_file):
    """Save extracted data to CSV file."""
    
    if not data_dict:
        print("No data to save!")
        return False
    
    try:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Email', 'Company']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data row
            writer.writerow(data_dict)
        
        print(f"✅ Successfully saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def display_extracted_data(data_dict):
    """Display extracted data in formatted output."""
    
    if not data_dict:
        print("No data to display!")
        return
    
    print("\n" + "="*50)
    print("EXTRACTED DATA SUMMARY")
    print("="*50)
    print(f"\n📝 Name:     {data_dict['Name']}")
    print(f"📧 Email:    {data_dict['Email']}")
    print(f"🏢 Company:  {data_dict['Company']}")
    print("="*50 + "\n")


def main():
    """Main function to run the Data Scavenger exercise."""
    
    # Define file paths
    input_file = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_data/L1_data/ex1_messy_profile.txt"
    output_csv = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_solutions_hermes/data_scavenger/ex01_name_email_company.csv"
    
    print("="*50)
    print("EXERCISE 1: DATA SCAVENGER - Clean Copy-Paste")
    print("="*50 + "\n")
    
    # Parse the messy profile data
    extracted_data = parse_profile_data(input_file)
    
    if extracted_data:
        # Display the results
        display_extracted_data(extracted_data)
        
        # Save to CSV
        save_to_csv(extracted_data, output_csv)
        
        print("🎉 Exercise completed successfully!")
    else:
        print("❌ Failed to extract data from input file.")


if __name__ == "__main__":
    main()
