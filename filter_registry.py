import json
from pathlib import Path

def main():
    # Read the GeoJSON file and extract TAXPINNO values
    print("Reading GeoJSON file...")
    with open('ond-parcels.geojson', 'r') as f:
        geojson_data = json.load(f)
    
    # Extract TAXPINNO values from features
    taxpinno_set = set()
    for feature in geojson_data['features']:
        if 'properties' in feature and 'TAXPINNO' in feature['properties']:
            taxpinno_set.add(feature['properties']['TAXPINNO'])
    
    print(f"Found {len(taxpinno_set)} unique TAXPINNO values")
    
    # Read and filter the registry file
    print("Reading and filtering registry file...")
    filtered_records = []
    
    with open('registry.json', 'r') as f:
        registry_data = json.load(f)
        
        for record in registry_data:
            if 'parcel' in record and record['parcel'] in taxpinno_set:
                filtered_records.append(record)
    
    print(f"Found {len(filtered_records)} matching records")
    
    # Write filtered results to a new file
    output_file = 'filtered_registry.json'
    print(f"Writing filtered results to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(filtered_records, f, indent=2)
    
    print("Done!")

if __name__ == "__main__":
    main() 