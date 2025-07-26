# GENERATES CSV REPORT

# External libraries
import csv
import os

# Internal library imports
from utility.terminal_outputs import printLine

def export_to_csv(filename, data, headers):
    """
    Exports data to a CSV file.

    :param filename: The name of the CSV file.
    :param data: A list of lists containing the data to write.
    :param headers: A list of column headers for the CSV file.
    """

    # Write data to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

    # Show finished export in terminal
    printLine()
    printLine(f"🟣 CSV data has been sucessfully written to:", True)
    printLine(f"🟣 {os.path.basename(filename)}", True)