#!/usr/bin/env python3
import json

# Read the extracted data
with open('extracted_excel_data.json', 'r') as f:
    data = json.load(f)

print(f"Original data: {len(data)} records")

# Clean the fault column - convert numeric values and invalid entries to "NA"
valid_faults = {"No Fault", "Electrical Fault", "Thermal Fault", "Partial discharge", "Spark discharge"}

for record in data:
    fault = str(record['Fault']).strip()
    
    # If it's not a valid fault type, set to NA
    if fault not in valid_faults:
        # Check if it's a number or invalid entry
        try:
            float(fault)  # If it's a number, it's invalid
            record['Fault'] = "NA"
        except ValueError:
            # If it's not a number but also not valid, check common patterns
            if fault in ['-', 'NA', '', 'None', 'null']:
                record['Fault'] = "NA"
            else:
                # Keep as is for now, might be a valid fault type we missed
                print(f"Unknown fault type: '{fault}'")
                record['Fault'] = "NA"

# Count final fault distribution
fault_counts = {}
for record in data:
    fault = record['Fault']
    fault_counts[fault] = fault_counts.get(fault, 0) + 1

print("Cleaned fault distribution:")
for fault, count in fault_counts.items():
    print(f"  {fault}: {count}")

# Save cleaned data
with open('cleaned_excel_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nCleaned data saved with {len(data)} records")

# Calculate statistics for all gas types
import statistics

gases = ['Hydrogen', 'Methane', 'Ethylene', 'Ethane', 'Acetylene']
stats = {}

for gas in gases:
    values = [record[gas] for record in data if record[gas] is not None]
    if values:
        stats[gas] = {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0
        }

print("\nGas concentration statistics:")
for gas, stat in stats.items():
    print(f"{gas}:")
    print(f"  Count: {stat['count']}")
    print(f"  Mean: {stat['mean']:.2f} ppm")
    print(f"  Median: {stat['median']:.2f} ppm")
    print(f"  Min: {stat['min']:.2f} ppm")
    print(f"  Max: {stat['max']:.2f} ppm")
    print(f"  Std Dev: {stat['std']:.2f} ppm")
    print()