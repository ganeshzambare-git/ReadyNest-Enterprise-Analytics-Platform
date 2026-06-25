import os
import glob
import re

views_dir = r"d:\Data Analytics Dashboard project\src\app\views"

for file_path in glob.glob(os.path.join(views_dir, "*.py")):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Remove st.set_page_config(...) block
    # It might span multiple lines, so we use DOTALL flag
    new_content = re.sub(r'st\.set_page_config\([^)]+\)', '', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Stripped set_page_config from {os.path.basename(file_path)}")
