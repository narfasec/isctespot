import sys
import os
def get_vat_rate(country_code):
    vat_rates = {
        'DE': 19,   # Germany
        'FR': 20,   # France
        'IT': 22,   # Italy
        'ES': 21,   # Spain
        'UK': 20,   # United Kingdom
        'NL': 21,   # Netherlands
        'SE': 25,   # Sweden
        'PT': 23,   # Portugal
        'BE': 21    # Belgium
    }

    # Normalize country code to uppercase and get the VAT rate
    country_code = country_code.upper()

    # Check if the country code exists in the dictionary
    return vat_rates.get(country_code, None)

def save_vat_to_file(vat_rate):
    with open('vat_rate.txt', 'w') as file:
        file.write(f"{vat_rate}")

def main():
    # Check if a country code argument was provided
    print('Executing vat ...')
    if len(sys.argv) != 2:
        print("Usage: python vat.py <country_code>")
        sys.exit(1)

    # Read the country code from the command line
    country_code = sys.argv[1].strip()

    # Get the VAT rate for the provided country code
    vat_rate = get_vat_rate(country_code)

    # Display the VAT rate or an error message
    if vat_rate is not None:
        save_vat_to_file(vat_rate)
        print(f"{vat_rate}")
    else:
        print(f"VAT rate for country code '{country_code}' is not available.")

if __name__ == "__main__":
    main()
