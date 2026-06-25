import os
import subprocess

commit = "8d2ab89"
views_dir = r"d:\Data Analytics Dashboard project\src\app\views"

mappings = {
    "00_Executive_Home.py": "00_Executive_Home.py",
    "0_Data_Loading.py": "01_Data_Ingestion.py",
    "1_Data_Cleaning.py": "03_Data_Cleaning.py",
    "2_Descriptive_Statistics.py": "04_Descriptive_Statistics.py",
    "3_Univariate_Analysis.py": "05_Univariate_Analysis.py",
    "4_Bivariate_Analysis.py": "06_Bivariate_Analysis.py",
    "5_Data_Visualization.py": "18_Advanced_Visual_Analytics.py",
    "6_Insight_Extraction.py": "20_Key_Insights.py",
    "07_Predictive_Modeling.py": "17_Predictive_Modeling_AI.py",
    "08_Advanced_Visuals.py": "19_Interactive_Dashboard.py",
    "09_Geographic_Intelligence.py": "15_Geographic_Intelligence.py",
    "10_Automated_Reporting.py": "22_Automated_Reporting.py",
    "11_Experimentation.py": "21_Business_Suggestions.py",
    "12_Data_Governance.py": "23_Governance_Security.py",
}

for old_name, new_name in mappings.items():
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:src/app/views/{old_name}"],
            cwd=r"d:\Data Analytics Dashboard project",
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        content = result.stdout
        
        n_path = os.path.join(views_dir, new_name)
        with open(n_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Restored {old_name} into {new_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract {old_name}: {e.stderr}")
