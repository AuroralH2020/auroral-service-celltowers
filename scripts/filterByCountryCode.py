import csv
import sys

# check if the number of arguments is correct
if len(sys.argv) != 4:
    print("Usage: filterByCountryCode.py inputFileName outputFileName countryCode")
    sys.exit(1)
# check if the input file exists
try:
    with open(sys.argv[1], 'r') as input_file:
        pass
except IOError:
    print("Input file does not exist")
    sys.exit(1)

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
countryCode = sys.argv[3]

# Open the input file
with open(inputFileName, 'r') as input_file:

    # Create a CSV reader object
    reader = csv.reader(input_file)

    # Open the output file
    with open(outputFileName, 'w', newline='') as output_file:

        # Create a CSV writer object
        writer = csv.writer(output_file)

        # Write the header row to the output file
        writer.writerow(next(reader))
        rows = 0
        # Iterate over the input rows and filter them based on a condition
        for row in reader:
            if row[1] == countryCode:
                # Write the filtered row to the output file
                writer.writerow(row)
                rows += 1
    # print number of filtered rows
    print("Number of filtered rows: " + str(rows))