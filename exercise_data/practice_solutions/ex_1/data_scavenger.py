import os
import re
import json
# We are assuming you have an LLM client setup (e.g., using OpenAI-compatible API endpoints 
# which many local servers like LM Studio expose). Replace this with your actual API client library.

def load_messy_data(file_path):
    """Loads the messy text file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {file_path}")
        return None

def extract_data_using_llm(messy_text):
    """
    SIMULATED FUNCTION: This function simulates calling an LLM API.
    In a real scenario, you would use a library like 'requests' to hit 
    your local server endpoint (e.g., http://localhost:1234/v1/chat/completions).
    """
    print("--- Running AI Extraction Simulation ---")

    # The critical element is the SYSTEM PROMPT and USER prompt construction.
    system_prompt = (
        "You are an expert data extraction specialist. Your task is to parse unstructured text "
        "and extract specific fields into a single, clean JSON object or CSV format. "
        "Only output the requested structured data."
    )
    user_prompt = f"""
    Analyze the following profile and extract:
    1. Full Name
    2. Primary Email Address
    3. Current Company Name

    The output MUST be a clean JSON object matching this schema: 
    {{ "Name": "string", "Email": "string", "Company": "string" }}. Do not include any conversational text, explanation, or markdown formatting outside of the JSON structure.

    --- PROFILE TEXT START ---
    {messy_text}
    --- PROFILE TEXT END ---
    """
    print(f"Sending prompt to local LLM server...")
    # ------------------------------------------------------
    # *** ACTION REQUIRED: REPLACE THIS BLOCK WITH REAL API CALLS ***
    # Example using a placeholder function call:
    # response = api_client.generate(system_prompt=system_prompt, user_content=user_prompt)
    # extracted_data = json.loads(response.text)
    
    # For demonstration purposes, we hardcode the successful extraction result:
    extracted_data = {
        "Name": "Alex Rivera",
        "Email": "alex.rivera@techflow.io",
        "Company": "TechFlow Solutions"
    }
    print("Extraction simulation complete.")
    return extracted_data
    # ------------------------------------------------------


def save_to_csv(data, output_file_path):
    """Saves the structured dictionary data into a CSV file."""
    if not data:
        print("No data provided to save.")
        return

    keys = list(data.keys())
    # Create header row
    header = ",".join(keys)
    # Create data row (ensure values are strings and properly escaped if necessary)
    row = ",".join([str(value).replace(",", "") for value in data.values()])

    csv_content = f"{header}\n{row}"

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        print(f"\n✅ Success! Clean data saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def main():
    """Main function to run the extraction process."""
    input_file = "exercise_data/L1_data/ex1_messy_profile.txt"
    output_dir = "exercise_data/practice_solutions"
    output_filename = "solution_ex1.csv"
    output_file_path = os.path.join(output_dir, output_filename)

    # 1. Load the source data
    messy_text = load_messy_data(input_file)

    if messy_text:
        # 2. Extract the data (AI step)
        extracted_data = extract_data_using_llm(messy_text)

        # 3. Save the results
        save_to_csv(extracted_data, output_file_path)

if __name__ == "__main__":
    main()