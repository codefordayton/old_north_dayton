import pandas as pd
import argparse
from lookup_coordinates import create_full_address

def geocode_row(row, coords_df):
    # Use the ADDRESS column for matching
    address = str(row['ADDRESS']).strip().lower()
    match = coords_df[coords_df['full_address'].str.strip().str.lower() == address]
    if not match.empty:
        return match.iloc[0]['latitude'], match.iloc[0]['longitude'], match.iloc[0]['TAXPINNO']
    return None, None, None

def main():
    parser = argparse.ArgumentParser(description='Geocode housing complaints using lookup_coordinates data')
    parser.add_argument('complaints_csv', help='Path to housingcomplaints.csv')
    parser.add_argument('--coords', default='output.csv', help='Path to coordinates CSV (default: output.csv)')
    parser.add_argument('--output', default='housingcomplaints_geocoded.csv', help='Output CSV path')
    args = parser.parse_args()

    # Load complaints and coordinates
    complaints = pd.read_csv(args.complaints_csv)
    coords = pd.read_csv(args.coords)

    # Generate full_address in coords for matching using the same logic as lookup_coordinates.py
    coords['full_address'] = coords.apply(create_full_address, axis=1)

    # Geocode each row
    print("Geocoding complaints...")
    results = complaints.apply(lambda row: geocode_row(row, coords), axis=1)
    complaints['latitude'] = results.apply(lambda x: x[0])
    complaints['longitude'] = results.apply(lambda x: x[1])
    complaints['TAXPINNO'] = results.apply(lambda x: x[2])

    # Save results
    complaints.to_csv(args.output, index=False, float_format='%.6f')
    print(f"Geocoded complaints saved to {args.output}")

if __name__ == "__main__":
    main() 