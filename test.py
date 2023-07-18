import csv
import os
import utils
import enum


class valid(enum.Enum):
    city = ['dubai', 'lahore', 'murree']
    options = ['1', '2', '3', '4', '5']


def convert_text_files_to_csv(directory_path, output_csv_path):
    # Create a list to store the data
    data = []

    # Define a mapping for quantifying the 'Events' column
    events_mapping = {
        '': 0,  # Empty value
        'Rain': 1,
        'Fog': 2,
        'Rain-Thunderstorm': 3,
        'Snow': 4,
        'Rain-Snow': 5,
        'Hail-Thunderstorm': 6,
        'Fog-Rain': 8,
        'Thunderstorm': 9,
        'Fog-Rain-Thunderstorm': 10,
        'Fog-Rain-Snow-Thunderstorm': 11,
        'Fog-Hail-Thunderstorm': 12,
        'Snow-Hail': 13,
        'Rain-Snow-Thunderstorm': 14,
        'Rain-Hail-Thunderstorm': 15,
        'Rain-Snow-Hail-Thunderstorm': 16,
        'Tornado': 17,
        'Rain-Thunderstorm-Tornado': 18,
        'Fog-Tornado': 19,
        'Rain-Thunderstorm-Tornado': 20,
        'Rain-Tornado': 21,
        'Thunderstorm-Tornado': 22,
    }

    # Initialize a flag to check if the header has been added
    header_added = False

    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                # Get the first line
                first_line = next(file).strip()

                # Check if the first line is empty
                if not first_line:
                    # Skip the first line
                    header = next(file)
                else:
                    header = first_line

                # Check if 'GST' or 'PKT' is present in the header
                if 'GST' in header:
                    # Replace 'GST' with 'Time' in the header
                    header = header.replace('GST', 'Time')
                elif 'PKT' in header:
                    # Replace 'PKT' with 'Time' in the header
                    header = header.replace('PKT', 'Time')
                elif 'PKST' in header:
                    # Replace 'PKT' with 'Time' in the header
                    header = header.replace('PKST', 'Time')
                # Append the modified header to the data list if it hasn't been added yet
                if not header_added:
                    data.append(header.strip().split(','))
                    header_added = True

                # Read each line and append it to the data list if it's not empty
                for line in file:
                    line = line.strip()
                    if line and "<" not in line:  # Skip empty rows and rows containing "<!--0.188:0-->"
                        # Split the line into columns
                        columns = line.split(',')
                        # Quantify the 'Events' column
                        events_value = columns[21].strip()
                        columns[21] = events_mapping.get(
                            events_value, events_value)
                        data.append(columns)

    # Write the data to the CSV file
    with open(output_csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the data rows
        writer.writerows(data)

    print('Data successfully stored in the CSV file.')


def to_csv():
    dir_paths = ['./Dubai_weather/', './lahore_weather', './Murree_weather']
    out_paths = ['./dubai.csv', './lahore.csv', './murree.csv']

    for i in range(len(dir_paths)):
        convert_text_files_to_csv(dir_paths[i], out_paths[i])


# Create the Csv files
# to_csv()


trigger = True


def check_city(city):
    if (city.lower() not in valid.city.value):
        print("Invalid city name")
        return False
    return True


def check_options(option):
    if (option not in valid.options.value):
        print("\nInvalid option\n")
        return False
    return True


def process_option(option, city):
    if (option == '1'):
        year = input("Enter the year: ")
        utils.get_max_temp(year, city)
    else:
        year = input("Enter the year: ")
        month = input("Enter the month: ")
        if (option == '2'):
            utils.get_monthly_avg(year, month, city)
        elif (option == '3'):
            utils.get_daily_max_min_no_Graph(year, month, city)
        elif (option == '4'):
            utils.get_daily_max_min_single(year, month, city)
        elif (option == '5'):
            utils.get_daily_max_min(year, month, city)


def is_continue():
    return input("\nDo you want to continue? (y to continue) ") == 'y'


def get_options():
    option = input(f"1. Get highest temp, lowest temp, and most humid day. \n"
                   "2. Get month wise average temperature. \n"
                   "3. Get daily max and min temperature. \n"
                   "4. Get daily max and min temperature in a single line \n"
                   "5. Get daily max and min with graph"
                   "\nEnter the option: ")

    return option


while (trigger):
    option = get_options()

    if (not check_options(option)):
        continue

    city = input("Enter the name of the city: ")

    if (not check_city(city)):
        continue

    process_option(option, city)

    trigger = is_continue()
