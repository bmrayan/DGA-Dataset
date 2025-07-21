#!/usr/bin/env python3
import json

# Read the cleaned Excel data
with open('cleaned_excel_data.json', 'r') as f:
    data = json.load(f)

print(f"Embedding {len(data)} records from Excel file...")

# Create the JavaScript array format
js_content = "const dgaData = [\n"
for i, record in enumerate(data):
    js_content += "  {\n"
    js_content += f'    "ID": {record["ID"]},\n'
    js_content += f'    "Hydrogen": {record["Hydrogen"]},\n'
    js_content += f'    "Methane": {record["Methane"]},\n'
    js_content += f'    "Ethylene": {record["Ethylene"]},\n'
    js_content += f'    "Ethane": {record["Ethane"]},\n'
    js_content += f'    "Acetylene": {record["Acetylene"]},\n'
    js_content += f'    "Fault": "{record["Fault"]}"\n'
    if i < len(data) - 1:
        js_content += "  },\n"
    else:
        js_content += "  }\n"

js_content += "];"

# Save to file
with open('embedded_data.js', 'w') as f:
    f.write(js_content)

print("JavaScript array saved to embedded_data.js")
print(f"Total size: {len(js_content)} characters")