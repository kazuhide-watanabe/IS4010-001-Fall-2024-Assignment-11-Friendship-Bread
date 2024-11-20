import csv
import re
import requests

def extract_missing_zip_addresses(data, output_path):
    """
    Identify rows in the 'Full Address' column that are missing zip codes.
    Extract the state and city for those rows and write them to a new CSV file.
    :param data: List of rows (including header).
    :param output_path: Path to save the new CSV file with missing zip addresses.
    """
    header = data[0]
    full_address_index = header.index("Full Address")  # Locate the "Full Address" column

    # Prepare header for the output file
    output_header = ["City", "State", "Full Address"]

    missing_zip_rows = []
    for row in data[1:]:
        full_address = row[full_address_index].strip()
        
        # Check if the address contains a zip code (5 consecutive digits)
        if not re.search(r"\b\d{5}\b", full_address):
            # Attempt to extract the state and city
            city, state = extract_city_and_state(full_address)
            missing_zip_rows.append([city, state, full_address])

    # Write rows with missing zip codes to the output CSV file
    with open(output_path, mode='w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_header)  # Write header
        writer.writerows(missing_zip_rows)  # Write rows with missing zips

    print(f"Missing zip addresses written to {output_path}")


def extract_city_and_state(full_address):
    """
    Attempt to extract the city and state from an address string.
    :param full_address: Address string.
    :return: Tuple (city, state).
    """
    # Pattern to match addresses like "City, State" or "City, State, Rest of Address"
    match = re.search(r"([a-zA-Z\s]+),\s*([A-Z]{2})", full_address)
    if match:
        city = match.group(1).strip()
        state = match.group(2).strip()
        return city, state
    return "", ""  # Return empty values if city and state cannot be parsed

API_URL_TEMPLATE = (
    "https://app.zipcodebase.com/api/v1/code/city"
    "?apikey=3f9cf660-a63c-11ef-9831-479c9c8e62aa"
    "&city={city}&state_name=Ohio&country=us"
)

def get_zip_code_for_city(city, cache):
    """
    Make an API call to retrieve the first zip code for a given city.
    If the city was already queried, return the cached result.
    :param city: City name to query.
    :param cache: Dictionary to store previously fetched zip codes.
    :return: First zip code found or None if no zip code is available.
    """
    # Check if the city is already in the cache
    if city in cache:
        print(f"Using cached zip code for city: {city}")
        return cache[city]

    # Construct the API URL
    url = API_URL_TEMPLATE.format(city=city)
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"API response for city {city}: {data}")

            # Extract zip codes from the 'results' key
            zip_codes = data.get("results", [])
            first_zip_code = zip_codes[0] if zip_codes else None

            # Cache the result for this city
            cache[city] = first_zip_code
            return first_zip_code
        except (KeyError, IndexError, ValueError) as e:
            print(f"Error parsing API response for city {city}: {e}")
    else:
        print(f"Failed API call for city {city} (Status Code: {response.status_code})")

    # Cache None if the API call fails
    cache[city] = None
    return None


def update_missing_zip_addresses(original_data, missing_zip_file, output_file):
    """
    Update addresses with missing zip codes by querying the API for zip codes.
    :param original_data: List of rows from the original data CSV.
    :param missing_zip_file: Path to the CSV file with missing zip addresses.
    :param output_file: Path to save the updated data with resolved zip codes.
    """
    # Read missing zip addresses
    with open(missing_zip_file, mode='r') as file:
        reader = csv.DictReader(file)
        missing_addresses = list(reader)

    # Create a map of "Full Address" to updated address with zip codes
    updated_addresses = {}
    city_cache = {}  # Cache for storing zip codes for each city

    for row in missing_addresses:
        city = row["City"]
        full_address = row["Full Address"]

        print(f"Processing city: {city}...")
        zip_code = get_zip_code_for_city(city, city_cache)
        if zip_code:
            updated_full_address = f"{full_address.strip()} {zip_code}"
            updated_addresses[full_address] = updated_full_address

    # Update original data with new addresses
    header = original_data[0]
    full_address_index = header.index("Full Address")

    updated_data = [header]
    for row in original_data[1:]:
        full_address = row[full_address_index].strip()
        if full_address in updated_addresses:
            row[full_address_index] = updated_addresses[full_address]
        updated_data.append(row)

    # Write updated data to the output file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_data)

    print(f"Updated data written to {output_file}")

