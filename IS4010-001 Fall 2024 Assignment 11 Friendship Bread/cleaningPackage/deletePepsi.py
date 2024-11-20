import csv

def handle_pepsi_purchases(data, anomalies_path):
    """
    Remove rows where "Fuel Type" contains 'Pepsi' and save them to a separate CSV file.
    :param data: List of rows (including header).
    :param anomalies_path: Path to save the anomalies CSV.
    :return: List of cleaned rows (excluding 'Pepsi' rows).
    """
    header = data[0]
    fuel_type_index = header.index("Fuel Type")  # Locate the "Fuel Type" column

    # Separate Pepsi rows and non-Pepsi rows
    pepsi_rows = []
    cleaned_data = [header]  # Start with the header

    for row in data[1:]:
        # Normalize the "Fuel Type" value for comparison
        fuel_type = row[fuel_type_index].strip().lower()
        if "pepsi" in fuel_type:
            pepsi_rows.append(row)
        else:
            cleaned_data.append(row)

    # Write anomalies (Pepsi rows) to the anomalies CSV file
    with open(anomalies_path, mode='w', newline='') as anomalies_file:
        writer = csv.writer(anomalies_file)
        writer.writerow(header)  # Write the header
        writer.writerows(pepsi_rows)  # Write Pepsi rows

    return cleaned_data






