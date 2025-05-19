import json
import csv
from collections import defaultdict

def main():
    # Read the filtered registry data
    print("Reading filtered registry data...")
    with open('filtered_registry.json', 'r') as f:
        registry_data = json.load(f)
    
    # Add type field to registry records
    for record in registry_data:
        record['type'] = 'registry'
    
    # Read and process housing complaints
    print("Reading housing complaints data...")
    complaints_by_parcel = defaultdict(list)
    
    with open('housingcomplaints_geocoded.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['TAXPINNO']:  # Only include complaints with a valid TAXPINNO
                complaint = {
                    'type': 'complaint',
                    'complaint_no': row['COMPLAINT_NO'],
                    'address': row['ADDRESS'],
                    'record_date': row['RECORD_DATE'],
                    'action_taken': row['ACTION_TAKEN'],
                    'status': row['STATUS'],
                    'assigned': row['ASSIGNED'],
                    'description': row['DESCRIPTION'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'TAXPINNO': row['TAXPINNO']
                }
                complaints_by_parcel[row['TAXPINNO']].append(complaint)
    
    # Merge the data
    print("Merging data...")
    merged_data = {
        'registry_records': registry_data,
        'complaints': []
    }
    
    # Add all complaints that match registry TAXPINNOs
    registry_taxpinnos = {record['TAXPINNO'] for record in registry_data}
    for taxpinno, complaints in complaints_by_parcel.items():
        if taxpinno in registry_taxpinnos:
            merged_data['complaints'].extend(complaints)
    
    # Write merged data to file
    output_file = 'merged_data.json'
    print(f"Writing merged data to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    # Print summary statistics
    print("\nSummary:")
    print(f"Registry records: {len(registry_data)}")
    print(f"Matching complaints: {len(merged_data['complaints'])}")
    print(f"Unique properties with complaints: {len({c['TAXPINNO'] for c in merged_data['complaints']})}")

if __name__ == "__main__":
    main() 