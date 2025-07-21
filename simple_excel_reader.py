#!/usr/bin/env python3
import zipfile
import xml.etree.ElementTree as ET
import json

def read_excel_data(filename):
    """Simple Excel reader using only built-in libraries"""
    try:
        # Excel files are ZIP archives
        with zipfile.ZipFile(filename, 'r') as z:
            # Get the shared strings (if any)
            shared_strings = []
            try:
                with z.open('xl/sharedStrings.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    # Namespace handling
                    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    for si in root.findall('.//s:si', ns):
                        t = si.find('.//s:t', ns)
                        if t is not None:
                            shared_strings.append(t.text)
            except:
                pass
            
            # Read the worksheet
            with z.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # Namespace
                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                
                data = []
                rows = root.findall('.//s:row', ns)
                
                print(f"Found {len(rows)} rows")
                
                for i, row in enumerate(rows):
                    row_data = []
                    cells = row.findall('.//s:c', ns)
                    
                    for cell in cells:
                        value = cell.find('.//s:v', ns)
                        cell_type = cell.get('t', '')
                        
                        if value is not None:
                            if cell_type == 's':  # Shared string
                                try:
                                    row_data.append(shared_strings[int(value.text)])
                                except:
                                    row_data.append(value.text)
                            else:
                                row_data.append(value.text)
                        else:
                            row_data.append('')
                    
                    data.append(row_data)
                    if i < 5:  # Print first 5 rows
                        print(f"Row {i+1}: {row_data}")
                
                return data
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

# Read the Excel file
filename = 'FinalDataSet_DGA.xlsx'
data = read_excel_data(filename)

if data:
    print(f"\nTotal rows: {len(data)}")
    
    # Convert to JSON format
    if len(data) > 1:  # Skip header row
        headers = data[0] if data[0] else ['ID', 'H2', 'CH4', 'C2H4', 'C2H6', 'C2H2', 'Fault']
        print(f"Headers: {headers}")
        
        json_data = []
        for i, row in enumerate(data[1:], 1):
            if len(row) >= 6:  # Ensure we have enough columns
                try:
                    record = {
                        "ID": i,
                        "Hydrogen": float(row[1]) if row[1] and row[1] != '' else 0.0,
                        "Methane": float(row[2]) if row[2] and row[2] != '' else 0.0,
                        "Ethylene": float(row[3]) if row[3] and row[3] != '' else 0.0,
                        "Ethane": float(row[4]) if row[4] and row[4] != '' else 0.0,
                        "Acetylene": float(row[5]) if row[5] and row[5] != '' else 0.0,
                        "Fault": str(row[6]) if len(row) > 6 and row[6] and row[6] != '' else "NA"
                    }
                    json_data.append(record)
                except ValueError as e:
                    print(f"Error processing row {i}: {e}, row data: {row}")
        
        # Save to file
        with open('extracted_excel_data.json', 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"\nExtracted {len(json_data)} records")
        if json_data:
            print("Sample record:", json_data[0])
            
            # Count faults
            fault_counts = {}
            for record in json_data:
                fault = record['Fault']
                fault_counts[fault] = fault_counts.get(fault, 0) + 1
            print("Fault distribution:", fault_counts)
else:
    print("Failed to read Excel file")