"""
Exercise 3: The "Note" Gatherer - Data Scavenger

Task: Take unstructured notes and create a task list in a new sheet with Status and Priority columns.

Input File: exercise_data/L1_data/ex3_unstructured_notes.txt
Output Format: CSV file with structured tasks including extracted actions, status, and priority
"""

import re
import csv


def parse_unstructured_notes(file_path):
    """Parse unstructured notes into structured task data."""
    
    tasks = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            
            if not line or not line.startswith('-'):
                continue  # Skip empty lines and non-bullet points
            
            # Extract the task description (remove leading "- ")
            task_match = re.match(r'-\s*(.+)', line)
            if not task_match:
                continue
            
            task_description = task_match.group(1).strip()
            
            # Extract Status from various formats
            status = "Not Started"  # Default status
            status_patterns = [
                r'Priority:\s*High\.?\s*Status:\s*(\w+(?:\s+\w+)?)',
                r'Priority:\s*[A-Za-z]+\.\s+Status:\s*(\w+(?:\s+\w+)?)',
                r'Status:\s*(\w+(?:\s+\w+)?)\.',
            ]
            
            for pattern in status_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    status_raw = match.group(1).strip()
                    # Normalize status values
                    status = normalize_status(status_raw)
                    break
            
            # Extract Priority from various formats
            priority = "Medium"  # Default priority
            
            # Check for urgent/ASAP keywords first
            if 'asap' in line.lower() or 'urgent' in line.lower():
                priority = 'High'
            elif 'critical' in line.lower():
                priority = 'Critical'
            
            # Try to extract explicit Priority field
            priority_match = re.search(r'Priority:\s*(\w+(?:\s+\w+)?)', line, re.IGNORECASE)
            if priority_match:
                priority_raw = priority_match.group(1).strip()
                priority = normalize_priority(priority_raw)
            
            # Add urgency indicators based on keywords
            urgency_keywords = ['ASAP', 'urgent', 'critical', 'by Friday']
            has_urgency = any(keyword.lower() in line.lower() for keyword in urgency_keywords)
            
            tasks.append({
                'Task_ID': f"T{line_num:03d}",
                'Description': task_description,
                'Status': status,
                'Priority': priority,
                'Urgent_Flag': '⚡ YES' if has_urgency else '',
                'Original_Line': line_num
            })
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None
    
    return tasks


def normalize_status(status_raw):
    """Normalize various status formats to standard values."""
    
    status_mapping = {
        'pending': 'Pending',
        'todo': 'To Do',
        'to do': 'To Do',
        'not started': 'Not Started',
        'in progress': 'In Progress',
        'progress': 'In Progress',
        'started': 'Started',
        'complete': 'Complete',
        'done': 'Done',
        'finished': 'Finished',
        'active': 'Active',
    }
    
    status_lower = status_raw.lower().strip()
    return status_mapping.get(status_lower, status_raw.capitalize())


def normalize_priority(priority_raw):
    """Normalize various priority formats to standard values."""
    
    # Check for critical/urgent keywords first
    if 'critical' in priority_raw.lower():
        return 'Critical'
    
    priority_mapping = {
        'high': 'High',
        'medium': 'Medium',
        'low': 'Low',
        'asap': 'High',  # ASAP maps to High priority
        'urgent': 'High',
    }
    
    priority_lower = priority_raw.lower().strip()
    return priority_mapping.get(priority_lower, 'Medium')


def calculate_priority_score(tasks):
    """Calculate a numeric priority score for sorting."""
    
    priority_scores = {
        'Critical': 100,
        'High': 75,
        'Medium': 50,
        'Low': 25
    }
    
    status_active = ['In Progress', 'To Do', 'Active']
    
    for task in tasks:
        priority_score = priority_scores.get(task['Priority'], 50)
        
        # Bonus points for urgent flag
        if task['Urgent_Flag']:
            priority_score += 20
        
        # Bonus points for active/in-progress status
        if task['Status'] in status_active:
            priority_score += 10
        
        task['Priority_Score'] = priority_score


def display_task_list(tasks):
    """Display the structured task list."""
    
    print("\n" + "="*90)
    print("STRUCTURED TASK LIST - EXCEL READY")
    print("="*90)
    
    # Sort by Priority Score (highest first)
    sorted_tasks = sorted(tasks, key=lambda x: x['Priority_Score'], reverse=True)
    
    # Print headers
    print(f"\n{'ID':<6} | {'Description':<45} | {'Status':<15} | {'Priority':<10}")
    print("-" * 90)
    
    for task in sorted_tasks:
        desc = task['Description'][:42] + "..." if len(task['Description']) > 45 else task['Description']
        print(f"{task['Task_ID']:<6} | {desc:<45} | {task['Status']:<15} | {task['Priority']:<10}")
    
    print("\n" + "="*90)


def generate_priority_summary(tasks):
    """Generate summary statistics organized by priority and status."""
    
    print("\n" + "="*80)
    print("TASK SUMMARY STATISTICS")
    print("="*80)
    
    # Count by Priority
    priority_counts = {}
    for task in tasks:
        p = task['Priority']
        priority_counts[p] = priority_counts.get(p, 0) + 1
    
    print(f"\n📊 Tasks by Priority:")
    for priority in ['Critical', 'High', 'Medium', 'Low']:
        if priority in priority_counts:
            bar = "█" * priority_counts[priority]
            print(f"   {priority:<10} | {bar} ({priority_counts[priority]})")
    
    # Count by Status
    status_counts = {}
    for task in tasks:
        s = task['Status']
        status_counts[s] = status_counts.get(s, 0) + 1
    
    print(f"\n📋 Tasks by Status:")
    for status in ['To Do', 'In Progress', 'Pending', 'Not Started']:
        if status in status_counts:
            bar = "█" * status_counts[status]
            print(f"   {status:<15} | {bar} ({status_counts[status]})")
    
    # Urgent tasks
    urgent_tasks = [t for t in tasks if t['Urgent_Flag']]
    print(f"\n⚡ Urgent Tasks (ASAP/Critical): {len(urgent_tasks)}")
    for task in urgent_tasks:
        print(f"   - {task['Description']}")
    
    print("\n" + "="*80)


def save_to_csv(tasks, output_file):
    """Save the structured tasks to CSV file."""
    
    try:
        if not tasks:
            return False
        
        # Define field names (exclude internal fields from display)
        fieldnames = ['Task_ID', 'Description', 'Status', 'Priority', 'Urgent_Flag']
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for task in tasks:
                # Only write the display fields
                row = {key: task[key] for key in fieldnames}
                writer.writerow(row)
        
        print(f"✅ Successfully saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def main():
    """Main function to run the Note Gatherer exercise."""
    
    # Define file paths
    input_file = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_data/L1_data/ex3_unstructured_notes.txt"
    output_csv = "/mnt/d/kabish_localmodel_exercise/localmodel_exercises/exercise_solutions_hermes/data_scavenger/ex03_note_gatherer.csv"
    
    print("="*90)
    print("EXERCISE 3: DATA SCAVENGER - The \"Note\" Gatherer")
    print("="*90 + "\n")
    
    # Parse unstructured notes
    tasks = parse_unstructured_notes(input_file)
    
    if tasks:
        # Calculate priority scores for sorting
        calculate_priority_score(tasks)
        
        # Display structured task list (sorted by priority)
        display_task_list(tasks)
        
        # Generate summary statistics
        generate_priority_summary(tasks)
        
        # Save to CSV
        save_to_csv(tasks, output_csv)
        
        print("\n🎉 Exercise completed successfully!")
    else:
        print("❌ Failed to parse notes.")


if __name__ == "__main__":
    main()
