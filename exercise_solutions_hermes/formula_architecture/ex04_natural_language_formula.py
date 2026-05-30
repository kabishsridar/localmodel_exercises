"""
Exercise 4: Natural Language Formulas - Formula Architect

Task: Write a formula that calculates a 15% discount but only if the 'Status' is 'Gold' 
      and the 'Total' is over $500.

Input File: exercise_data/L1_data/ex4_sales_status.csv
Output Format: CSV with new column 'Discounted_Total' showing the price after 15% discount
"""

import pandas as pd
import csv


def load_csv_data(file_path):
    """Load CSV data into a DataFrame."""
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None


def apply_natural_language_formula(df):
    """Apply the formula: 15% discount if Status='Gold' AND Total > $500."""
    
    # Create a new column for Discounted_Total
    df['Discounted_Total'] = df.apply(
        lambda row: row['Total'] * 0.85 
                    if (row['Status'] == 'Gold' and row['Total'] > 500) 
                    else row['Total'],
        axis=1
    )
    
    # Create a column to show the discount amount
    df['Discount_Amount'] = df.apply(
        lambda row: round(row['Total'] * 0.15, 2) 
                    if (row['Status'] == 'Gold' and row['Total'] > 500) 
                    else 0.00,
        axis=1
    )
    
    # Create a column to show whether discount was applied
    df['Discount_Applicable'] = df.apply(
        lambda row: "✅ YES" 
                    if (row['Status'] == 'Gold' and row['Total'] > 500) 
                    else "❌ NO",
        axis=1
    )
    
    return df


def display_formula_results(df):
    """Display the results with formula explanation."""
    
    print("\n" + "="*90)
    print("FORMULA ARCHITECT - Natural Language Formulas")
    print("="*90)
    print("\n📋 FORMULA APPLIED:")
    print("   IF Status='Gold' AND Total > $500 THEN apply 15% discount")
    print("   Formula: =IF(AND(Status=\"Gold\", Total>500), Total*0.85, Total)")
    print("="*90 + "\n")
    
    # Display formatted table
    display_cols = ['Status', 'Total', 'Customer ID', 'Discounted_Total', 'Discount_Amount', 'Discount_Applicable']
    
    print(f"{'ID':<6} | {'Status':<8} | {'Total':>10} | {'Disc. Total':>12} | {'Discount':>10} | {'Applied?':<10}")
    print("-" * 90)
    
    for idx, row in df.iterrows():
        customer_id = str(row['Customer ID'])[:8]
        total = f"${row['Total']:,.2f}"
        disc_total = f"${row['Discounted_Total']:,.2f}"
        discount_amt = f"${row['Discount_Amount']:,.2f}"
        
        print(f"CUST{customer_id:<7} | {row['Status']:<8} | {total:>10} | {disc_total:>12} | {discount_amt:>10} | {row['Discount_Applicable']:<10}")
    
    print("\n" + "="*90)


def calculate_summary_stats(df):
    """Calculate summary statistics for the discount application."""
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    # Total original amount
    total_original = df['Total'].sum()
    
    # Total discounted amount
    total_discounted = df['Discounted_Total'].sum()
    
    # Total discount given
    total_discount = (df['Total'] - df['Discounted_Total']).sum()
    
    # Number of customers who got discount
    discount_eligible = len(df[(df['Status'] == 'Gold') & (df['Total'] > 500)])
    
    # Breakdown by status
    gold_customers = len(df[df['Status'] == 'Gold'])
    silver_customers = len(df[df['Status'] == 'Silver'])
    bronze_customers = len(df[df['Status'] == 'Bronze'])
    
    print(f"\n💰 Financial Summary:")
    print(f"   📊 Total Original Amount:      ${total_original:,.2f}")
    print(f"   💵 Total After Discount:       ${total_discounted:,.2f}")
    print(f"   🎁 Total Discount Given:       ${total_discount:,.2f}")
    
    print(f"\n👥 Customer Analysis:")
    print(f"   ⭐ Gold Customers (> $500):      {discount_eligible} of {gold_customers} eligible for discount")
    print(f"   🥈 Silver Customers:             {silver_customers}")
    print(f"   🥉 Bronze Customers:             {bronze_customers}")
    
    # Calculate savings percentage
    if total_original > 0:
        savings_pct = (total_discount / total_original) * 100
        print(f"\n📈 Overall Savings Rate:          {savings_pct:.2f}%")
    
    print("\n" + "="*80)


def save_to_csv(df, output_file):
    """Save the results to CSV file."""
    
    try:
        # Select only relevant columns for output
        output_cols = ['Status', 'Total', 'Customer ID', 'Discounted_Total', 'Discount_Amount', 'Discount_Applicable']
        
        df[output_cols].to_csv(output_file, index=False)
        
        print(f"✅ Successfully saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def generate_excel_formula():
    """Generate the Excel formula for users to copy-paste."""
    
    print("\n" + "="*80)
    print("EXCEL FORMULA TO COPY-PASTE")
    print("="*80)
    
    formulas = {
        "Basic Formula": "=IF(AND(A2=\"Gold\", B2>500), B2*0.85, B2)",
        "With Rounding": "=IF(AND(A2=\"Gold\", B2>500), ROUND(B2*0.85, 2), B2)",
        "Discount Amount": "=IF(AND(A2=\"Gold\", B2>500), B2*0.15, 0)",
        "Conditional Formatting Rule": "Status = \"Gold\" AND Total > 500"
    }
    
    print("\n📝 Assuming your data starts at Row 2 with:")
    print("   Column A: Status")
    print("   Column B: Total")
    print()
    
    for label, formula in formulas.items():
        print(f"{label:<25} {formula}")
    
    print("\n" + "="*80)


def main():
    """Main function to run the Natural Language Formulas exercise."""
    
    # Define file paths
    input_file = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_data/L1_data/ex4_sales_status.csv"
    output_csv = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_solutions_hermes/formula_architecture/ex04_natural_language_formula.csv"
    
    print("="*90)
    print("EXERCISE 4: FORMULA ARCHITECT - Natural Language Formulas")
    print("="*90 + "\n")
    
    # Load data
    df = load_csv_data(input_file)
    
    if df is not None:
        # Apply the formula
        df = apply_natural_language_formula(df)
        
        # Display results
        display_formula_results(df)
        
        # Calculate and show summary statistics
        calculate_summary_stats(df)
        
        # Generate Excel formulas for reference
        generate_excel_formula()
        
        # Save to CSV
        save_to_csv(df, output_csv)
        
        print("\n🎉 Exercise completed successfully!")
    else:
        print("❌ Failed to load data.")


if __name__ == "__main__":
    main()
