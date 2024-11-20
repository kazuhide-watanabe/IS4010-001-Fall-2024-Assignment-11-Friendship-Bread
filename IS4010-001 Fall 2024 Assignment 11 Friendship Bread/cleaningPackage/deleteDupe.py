def delete_duplicates(data):
    """
    Remove duplicate rows from the data.
    :param data: List of rows (including header).
    :return: List of unique rows (including header).
    """
    seen = set()
    unique_data = []
    for row in data:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            unique_data.append(row)
            seen.add(row_tuple)
    return unique_data





