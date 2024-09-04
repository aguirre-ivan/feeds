import csv
import sys
import os

COUNTRY_ISO_FILE = 'country_iso.csv'
FIELDS_TO_REPLACE = ['baselinecountries', 'targetcountries', 'achievedcountries', 'trackcountries', 'riskcountries', 'noprogresscountries']

def build_country_dict():
    country_dict = {}
    with open(COUNTRY_ISO_FILE, 'r') as f:
        for line in f:
            line = line.strip().replace('"', '')
            iso, country = line.strip().split('|', 1)
            country_dict[iso] = country
    return country_dict

def replace_country_iso(feed_file):
    country_dict = build_country_dict()
    
    output_file = os.path.splitext(feed_file)[0] + '_replaced.csv'
    
    with open(feed_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        if not fieldnames:
            raise ValueError("No fieldnames found in the CSV file")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as g:
            writer = csv.DictWriter(g, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                for field in fieldnames:
                    if field in row:
                        original_value = row[field]
                        trimmed_value = original_value.strip()
                        if trimmed_value != original_value:
                            print(f"Field trimmed: {field}, Original: '{original_value}', Trimmed: '{trimmed_value}'")
                        row[field] = trimmed_value

                for field in FIELDS_TO_REPLACE:
                    if field in row and row[field]:
                        # Replace ISO codes with country names
                        original_value = row[field]
                        iso_codes = original_value.split('|')
                        country_names = []
                        for iso in iso_codes:
                            country_name = country_dict.get(iso)
                            if country_name:
                                country_names.append(country_name)
                            else:
                                # If ISO code not found, print it
                                print(f"ISO code not found: {iso}")
                                country_names.append(iso)  # Keep the original ISO code
                        row[field] = '|'.join(country_names)
                
                writer.writerow(row)
    
    print(f"Replaced file created: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <feed_file.csv>")
        sys.exit(1)
    
    feed_file = sys.argv[1]
    replace_country_iso(feed_file)

if __name__ == '__main__':
    main()
