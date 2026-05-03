# Exercise 2: Browser-to-Sheet (Data Scavenger)\n\n## Objective
To use the Pi for Excel add-in to read unstructured, messy data pasted from a web browser or other source into an Excel sheet and automatically format it into clean, structured columns with proper headers.\n\n## Prerequisites
1.  **Pi for Excel:** The AI add-in must be installed and connected to your local model server (e.g., LM Studio).
2.  **Source Data:** You must have a sample block of messy data copied to your system clipboard. This data should not currently be in an ideal table format.\n\n## Steps to Solve the Problemn\n### Step 1: Prepare the Sheet and Copy Data
*   Open a new Excel sheet (or use a dedicated area for this exercise).\n*   In a web browser, find some sample text that is messy or poorly formatted (e.g., contact details from a directory listing, product specs copied as a paragraph). **Copy this entire block of unstructured data to your clipboard.**\n*   Select the target cell in Excel where the clean table should begin.\n\n### Step 2: Invoke the Pi Function
*   Use the dedicated Pi feature (either via the Ribbon button or sidebar prompt). This is the point where you engage the AI agent's data processing capabilities.\n*   **Prompt:** Enter the following clear instruction into the Pi prompt box:\n    > \n\n### Step 3: Review and Refine (The Output)
*   Pi will process the data from the clipboard *contextually*. It reads the messiness and applies its understanding of typical data structure.
*   The AI should generate a clean, separated table directly into the spreadsheet cells.\n*   **Verification:** Check that:
    1.  All unique pieces of information are accounted for.
    2.  Each logical category (e.g., 'Name', 'Email', 'Date') has been assigned its own header and column.
\n\n## 💡 Key Takeaway
This exercise demonstrates Pi's ability to act as an intelligent data cleaner, converting free-form text into actionable spreadsheet structure without manual parsing or formula writing.
