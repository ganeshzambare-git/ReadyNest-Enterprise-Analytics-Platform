import os
import re

legacy_dir = r"d:\Data Analytics Dashboard project\src\app\legacy_views"
views_dir = r"d:\Data Analytics Dashboard project\src\app\views"

mappings = {
    "1_Data_Cleaning.py": "03_Data_Cleaning.py",
    "2_Descriptive_Statistics.py": "04_Descriptive_Statistics.py",
    "3_Univariate_Analysis.py": "05_Univariate_Analysis.py",
    "4_Bivariate_Analysis.py": "06_Bivariate_Analysis.py",
    "5_Data_Visualization.py": "18_Advanced_Visual_Analytics.py",
    "6_Insight_Extraction.py": "20_Key_Insights.py",
    "07_Predictive_Modeling.py": "17_Predictive_Modeling_AI.py",
    "09_Geographic_Intelligence.py": "15_Geographic_Intelligence.py",
    "10_Automated_Reporting.py": "22_Automated_Reporting.py",
    "11_Experimentation.py": "21_Business_Suggestions.py",
    "12_Data_Governance.py": "23_Governance_Security.py",
}

for legacy_file, new_file in mappings.items():
    l_path = os.path.join(legacy_dir, legacy_file)
    n_path = os.path.join(views_dir, new_file)
    
    if not os.path.exists(l_path) or not os.path.exists(n_path):
        print(f"Skipping {legacy_file} -> {new_file} (Not found)")
        continue
        
    with open(l_path, "r", encoding="utf-8") as f:
        l_content = f.read()
        
    with open(n_path, "r", encoding="utf-8") as f:
        n_content = f.read()
        
    # Extract title, desc, bv from new file
    title_match = re.search(r'title="([^"]+)"', n_content)
    desc_match = re.search(r'description="([^"]+)"', n_content)
    bv_match = re.search(r'business_value="([^"]+)"', n_content)
    
    title = title_match.group(1) if title_match else "Dashboard"
    desc = desc_match.group(1) if desc_match else ""
    bv = bv_match.group(1) if bv_match else "Enterprise value"
    
    # Clean up legacy content:
    # 1. Remove st.set_page_config(...)
    l_content = re.sub(r'st\.set_page_config\([^)]+\)', '', l_content, flags=re.DOTALL)
    
    # 2. Remove st.title(...)
    l_content = re.sub(r'st\.title\([^)]+\)', '', l_content)
    
    # 3. Remove standalone st.caption(...) right after title (heuristically)
    # Actually let's just leave captions alone or manually remove them later if needed.
    # It's safer to just remove st.set_page_config and st.title.
    
    # Construct new file
    new_code = f"""import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer

st.set_page_config(page_title="{title} - ReadyNest", layout="wide")

render_header(
    title="{title}",
    description="{desc}",
    business_value="{bv}"
)

# --- RESTORED LEGACY LOGIC ---
{l_content}

# --- FOOTER ---
render_footer("{title}")
"""

    with open(n_path, "w", encoding="utf-8") as f:
        f.write(new_code)
        
    print(f"Migrated {legacy_file} -> {new_file}")
