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
    missing_zip_csv = 'Data/missingZipAddresses.csv'

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
    
    
    # Process the data to find addresses missing zip codes
    extract_missing_zip_addresses(data, missing_zip_csv)
    print(f"Missing zip addresses written to {missing_zip_csv}")

    # Update missing zip codes
    update_missing_zip_addresses(data, missing_zip_csv, cleaned_csv)

if __name__ == "__main__":
    main()
