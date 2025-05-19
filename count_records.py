import json

def main():
    # Count records in registry.json
    print("Counting records in registry.json...")
    with open('registry.json', 'r') as f:
        registry_data = json.load(f)
        registry_count = len(registry_data)
    
    # Count records in filtered_registry.json
    print("Counting records in filtered_registry.json...")
    with open('filtered_registry.json', 'r') as f:
        filtered_data = json.load(f)
        filtered_count = len(filtered_data)
    
    print(f"\nResults:")
    print(f"registry.json: {registry_count:,} records")
    print(f"filtered_registry.json: {filtered_count:,} records")
    print(f"Percentage kept: {(filtered_count/registry_count)*100:.1f}%")

if __name__ == "__main__":
    main() 