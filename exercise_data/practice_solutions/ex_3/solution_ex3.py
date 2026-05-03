import pyperclip
import csv
import re
import os
from io import StringIO

def extract_clipboard_data(text):
    """
    Analyzes clipboard text. It first checks if the data is already structured 
    (like a TSV table copied from a browser/Excel). If so, it parses it natively.
    Otherwise, it simulates intelligence by extracting entities from unstructured text.
    """
    if not text or len(text.strip()) < 10:
        return None, "Error: Clipboard content is too short or empty."

    # --- Heuristic Check for Structured Tabular Data (TSV / CSV) ---
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    if len(lines) > 1:
        tab_counts = [line.count('\t') for line in lines]
        if tab_counts[0] > 0 and all(c == tab_counts[0] for c in tab_counts):
            try:
                reader = csv.DictReader(StringIO(text.strip()), delimiter='\t')
                extracted_records = [row for row in reader]
                if extracted_records:
                    return extracted_records, "Success (Parsed as Tab-Separated Data)"
            except Exception:
                pass
                
        comma_counts = [line.count(',') for line in lines]
        if comma_counts[0] > 0 and all(c == comma_counts[0] for c in comma_counts):
            try:
                reader = csv.DictReader(StringIO(text.strip()), delimiter=',')
                extracted_records = [row for row in reader]
                if extracted_records:
                    return extracted_records, "Success (Parsed as Comma-Separated Data)"
            except Exception:
                pass

    # --- Fallback: Extract from Unstructured Text ---
    extracted_records = []
    
    # Regex patterns to find common entities
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+" 
    company_pattern = r"([A-Z][a-zA-Z]*\s+(?:Corp|Solutions|Inc|LLC|Company|Enterprises|Ltd|Corporation))"
    date_pattern = r"(\d{2}/\d{2}/\d{4}|\d{1,2}-\d{2}-\d{4}|\d{4}-\d{2}-\d{2})"
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    name_pattern = r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b"

    company_keywords = ['Corp', 'Solutions', 'Inc', 'LLC', 'Company', 'Enterprises', 'Ltd', 'Corporation']

    emails = list(re.finditer(email_pattern, text))
    
    if not emails:
        return None, "Error: No email addresses found to anchor records. Please ensure unstructured data contains emails, or that tabular data is correctly formatted."

    # Create boundaries to chunk the text around each email
    boundaries = [0]
    for i in range(len(emails) - 1):
        mid = (emails[i].end() + emails[i+1].start()) // 2
        boundaries.append(mid)
    boundaries.append(len(text))
    
    for i, email_match in enumerate(emails):
        chunk = text[boundaries[i]:boundaries[i+1]]
        data = {}
        
        # Extract entities within this chunk
        companies = re.findall(company_pattern, chunk)
        data['Name'] = "N/A"
        data['Company'] = companies[0] if companies else "N/A"
        
        raw_names = re.findall(name_pattern, chunk)
        valid_names = [n for n in raw_names if n not in companies and not any(kw in n for kw in company_keywords)]
        if valid_names:
            data['Name'] = valid_names[0]

        data['Email Address'] = email_match.group(0)
        
        dates = re.findall(date_pattern, chunk)
        data['Start Date'] = dates[0] if dates else "N/A"
        
        phones = re.findall(phone_pattern, chunk)
        data['Phone Number'] = phones[0] if phones else "N/A"
        
        extracted_records.append(data)

    return extracted_records, "Success (Extracted from Unstructured Text)"


def save_to_csv(data, filename):
    """Saves a list of dictionaries to a CSV file."""
    if not data:
        print("No data provided to save.")
        return

    # Use the keys from the first dictionary as headers
    fieldnames = list(data[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully saved structured data to {filename}")


def main():
    """Main function to read clipboard and process/save the solution."""
    print("--- Running Exercise 2: Browser-to-Sheet Solution Generator ---")
    print("NOTE: This script requires sample messy data in the system clipboard.")

    try:
        # Attempt to retrieve content from the system clipboard
        clipboard_text = pyperclip.paste()
        if not clipboard_text or not clipboard_text.strip():
             raise ValueError("Clipboard is empty.")
    except pyperclip.PyperclipException as e:
        print(f"Error accessing clipboard (Is 'pyperclip' installed?): {e}")
        print("Falling back to simulated data for demonstration...")
        # Fallback simulation if clipboard access fails
        clipboard_text = "John Doe is located at Acme Corp (acme@example.com). He started on 10/01/2022 and his direct line is 555-1234. Contact Jane Smith, who works for Beta Solutions in Boston. Her details are jane@betasolutions.net. She has been with the company since 05/15/2023."
    except Exception as e:
        print(f"An unexpected error occurred during clipboard reading: {e}")
        print("Falling back to simulated data for demonstration...")
        clipboard_text = "John Doe is located at Acme Corp (acme@example.com). He started on 10/01/2022 and his direct line is 555-1234. Contact Jane Smith, who works for Beta Solutions in Boston. Her details are jane@betasolutions.net. She has been with the company since 05/15/2023."

    # Extract and structure the data
    structured_data, status = extract_clipboard_data(clipboard_text)
    
    if structured_data is None:
        print(status)
        return

    print(f"\n[STATUS] Data extracted successfully! ({status})")
    
    # Save the output to a CSV file
    output_dir = os.path.join("exercise_data", "practice_solutions", "ex_2")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "ex3_solution_output.csv")
    
    save_to_csv(structured_data, output_file)
    
    print("\n===============================================")
    print("PROCESS COMPLETE:")
    print(f"The structured solution has been written to {output_file}.")
    print("This CSV file can be imported directly into Excel.")


if __name__ == "__main__":
    # Check for dependency and install if needed (in a real environment)
    try:
        import pyperclip
    except ImportError:
        print("\n[DEPENDENCY MISSING] Please install the 'pyperclip' library: pip install pyperclip")
        exit()

    main()