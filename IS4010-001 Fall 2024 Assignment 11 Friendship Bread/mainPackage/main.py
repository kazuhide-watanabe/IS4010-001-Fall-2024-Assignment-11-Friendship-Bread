import csv
from cleaningPackage.deleteDupe import *
from cleaningPackage.deletePepsi import *
from cleaningPackage.twoDecimal import *
from cleaningPackage.updateZip import *


def main():
    # Paths to data files
    input_csv = 'Data/fuelPurchaseData.csv'
    anomalies_csv = 'Data/dataAnomalies.csv'
    cleaned_csv = 'Data/cleanedData.csv'

    # Load the dataset
    with open(input_csv, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Step 1: Format "Gross Price" to two decimal places
    data = format_gross_price(data)

    # Step 2: Remove rows with Pepsi purchases and log them to dataAnomalies.csv
    data = handle_pepsi_purchases(data, anomalies_csv)

    # Step 3: Remove duplicate rows
    data = delete_duplicates(data)

    # Save cleaned data
    with open(cleaned_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("Data cleanup completed. Cleaned data saved to:", cleaned_csv)

if __name__ == "__main__":
    main()

    # Set the API URL
    url = 'https://app.zipcodebase.com/api/v1/status?apikey=3f9cf660-a63c-11ef-9831-479c9c8e62aa'
    api = API(url)

    # Fetch data from the API
    data = api.fetchData()

    # Extract relevant data: comic titles and character counts
    extractedData, characterCounts = api.extractData(data)

    # Print extracted comic titles
    print("Comic Titles:")
    for item in extractedData:
        print(item["title"])

    # Print character counts
    print("\nCharacter Counts:")
    for character, count in characterCounts.items():
        print(f"{character}: {count}")
