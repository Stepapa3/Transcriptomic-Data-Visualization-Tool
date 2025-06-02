import csv

def detect_delimiter(file):
    """
    Detects the delimiter used in a CSV file.

    Parameters:
    file (UploadedFile): uploaded file

    Returns:
    str: Detected delimiter. Defaults to ',' if detection fails.
    """
    # Read a sample from the beginning of the file for delimiter detection
    sample = file.read(2048).decode("utf-8", errors="ignore")  # Read 2048 bytes and decode as text
    file.seek(0)  # Reset the file cursor to the beginning for future reads

    sniffer = csv.Sniffer()
    try:
        # Try to detect the delimiter from common options
        dialect = sniffer.sniff(sample, delimiters=[",", ";", "\t"])
        return dialect.delimiter
    except csv.Error:
        # If detection fails, use comma
        return ","

