import re

filepath = r'd:\Data Analytics Dashboard project\src\app\components\global_header.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all href="http://localhost:3000/..." with href="#" onclick="..."
new_content = re.sub(
    r'href="http://localhost:3000/[^"]*"',
    r'href="#" onclick="alert(\'Next.js routing pending scaffolding.\'); return false;"',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Replaced links successfully.")
