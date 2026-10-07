# HR Analytics Dashboard

An interactive HR analytics dashboard built from the cleaned HR Analytics dataset. The project presents employee count, attrition, attrition rate, demographic trends, salary trends, job-role attrition, job satisfaction and years-at-company analysis.

## Dashboard

The original Power BI report is included as `HR_Dashboard.pbix`.

The Python recreation is available as `app.py` and can be run in VS Code with Streamlit.

## Features

- Department filter
- Employee Count KPI
- Attrition KPI
- Attrition Rate KPI
- Average Age KPI
- Average Salary KPI
- Average Years at Company KPI
- Attrition by Education Field
- Attrition by Age Group
- Attrition by Gender
- Job Role & Job Satisfaction table
- Attrition by Job Role
- Attrition by Salary Slab
- Attrition by Years at Company

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- Power BI
- Power Query / data cleaning
- DAX in the original Power BI report

## Dataset

`HR_Analytics_Final_Cleaned.csv` is the cleaned dataset used by the Python dashboard. The dataset contains employee demographics, department, job role, salary, satisfaction, attrition and tenure-related fields.

## Project Structure

```text
HR-Analytics-Dashboard/
│
├── app.py
├── HR_Analytics_Final_Cleaned.csv
├── HR_Dashboard.pbix
├── requirements.txt
├── README.md
└── Project_Report.pdf
```

## Run in VS Code

1. Install Python 3.10 or newer.
2. Open this project folder in VS Code.
3. Open the VS Code terminal.
4. Create a virtual environment:

```bash
python -m venv venv
```

5. Activate it on Windows:

```bash
venv\Scripts\activate
```

6. Install dependencies:

```bash
pip install -r requirements.txt
```

7. Run the dashboard:

```bash
streamlit run app.py
```

8. Open the local URL shown in the terminal, normally `http://localhost:8501`.

## Power BI Report

Open `HR_Dashboard.pbix` using Microsoft Power BI Desktop to view the original Power BI dashboard.

## Important Note

`HR_Dashboard.pbix` is the actual Power BI report. `app.py` is a Python/Streamlit recreation of the report for environments that require a source-code submission. A Python program cannot execute a PBIX file itself; Power BI Desktop is required for the PBIX report.

## Author

Vaishnavi Raga
