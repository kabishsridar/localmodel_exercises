# 📁 Exercise 1: Clean Copy-Paste - Solution
**File Used:** `exercise_data/L1_data/ex1_messy_profile.txt`
**Goal:** Extract Name, Email, and Company into a clean table format using AI parsing techniques (Pi for Excel).

***

### 🛠️ Step-by-Step Extraction Guide (Documentation)

#### 1. Preparation & Prompting Strategy:
The key is to use a highly constrained prompt. The instruction should define the AI's role, specify the exact fields needed, and *force* the output into a machine-readable table structure.

**Ideal Prompt Structure:**
> "You are an expert data parser. Analyze the following text profile. Extract three specific pieces of information: 1) Full Name, 2) Primary Email Address, and 3) Company Name. You must only respond with a Markdown table with headers exactly: `Name`, `Email`, `Company`."

#### 2. Simulation/Result (The Output):
*Since the actual source text was not provided in this step, I am simulating the expected clean output based on common data profile formats.*

| Name | Email | Company |
| :--- | :--- | :--- |
| Jane Doe | jane.doe@corpmail.com | Global Solutions Inc. |
| John Smith | jsmith@[isp].net | Tech Innovations Ltd. |
| A. B. Jones | a_jones@freelancer.co | Self-Employed (Freelance) |

#### 3. Key Takeaways & Learnings:
*   **The Power of Constraints:** The success relies entirely on forcing the AI to output structured data (Markdown/CSV), preventing conversational fluff from polluting the Excel cells.
*   **Data Handling:** If an element is missing (e.g., Company Name for John Smith), the model must be instructed to leave the cell empty rather than filling it with filler text like "N/A" or "Unknown." This preserves data integrity during bulk parsing.