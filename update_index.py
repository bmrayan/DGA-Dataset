#!/usr/bin/env python3

# Read the original index.html
with open('index.html', 'r') as f:
    lines = f.readlines()

print(f"Original file has {len(lines)} lines")

# Find the start and end of the data section
start_line = None
end_line = None

for i, line in enumerate(lines):
    if line.strip() == "const dgaData = [":
        start_line = i
        print(f"Found data start at line {i+1}")
    elif line.strip() == "];" and start_line is not None and end_line is None:
        end_line = i
        print(f"Found data end at line {i+1}")
        break

if start_line is None or end_line is None:
    print("Could not find data section boundaries")
    exit(1)

# Read the new data
with open('embedded_data.js', 'r') as f:
    new_data = f.read()

# Split the new data into lines
new_data_lines = new_data.split('\n')

# Create the new file
new_lines = []
new_lines.extend(lines[:start_line])  # Everything before the data
new_lines.extend([line + '\n' for line in new_data_lines])  # New data
new_lines.extend(lines[end_line+1:])  # Everything after the data

print(f"New file will have {len(new_lines)} lines")
print(f"Replaced {end_line - start_line + 1} lines with {len(new_data_lines)} lines")

# Save the updated file
with open('index.html', 'w') as f:
    f.writelines(new_lines)

print("Updated index.html with real Excel data")