import pandas as pd
import matplotlib.pyplot as plt
from colorama import Fore, Style


def visualise_temp(value):
    output = ""
    value = abs(value)
    for i in range(value):
        output += "+"
    return output


def visualise_temp_single(value, high):
    output = ""
    value = abs(value)
    for i in range(value):
        output += "+"
    if (high):
        return (Fore.RED + output)
    else:
        return (Fore.BLUE + output)


def display_max_min_temp(year, max_temp, max_temp_day, min_temp, min_temp_day, max_humidity_day, max_humidity_value):
    print("For the year", year)
    print("Highest temperature:", max_temp, "°C on", max_temp_day)
    print("Lowest temperature:", min_temp, "°C on", min_temp_day)
    print("Most humid day:", max_humidity_day,
          "with humidity", max_humidity_value)


def display_monthly_avg_temp(year, month, avg_max_temp, avg_min_temp, avg_humidity):
    print(f"For the month {month} / {year}")
    print(f"Average highest temperature: {avg_max_temp} °C")
    print(f"Average lowest temperature: {avg_min_temp} °C")
    print(f"Average humidity: {avg_humidity}")


def display_daily_max_min_temp(days, max_temps, min_temps):
    print("\n")
    # for each day display the highest and lowest temperature
    for i in range(len(days)):
        print(
            f"{days[i]}: Highest: {Fore.RED + visualise_temp(int(max_temps[i]))} {max_temps[i]} °C, ")
        print(
            f"{days[i]}: Lowest: {Fore.BLUE + visualise_temp(int(min_temps[i]))} {min_temps[i]} °C, ")

    print(Style.RESET_ALL)


def display_daily_max_min_temp_single(days, max_temps, min_temps):
    print("\n")
    # for each day display the highest and lowest temperature
    for i in range(len(days)):
        print(f"{days[i]}: {visualise_temp_single(int(min_temps[i]), False)} {visualise_temp_single(int(max_temps[i]), True)} {Style.RESET_ALL} \t {min_temps[i]} °C - {max_temps[i]} °C ")

    print(Style.RESET_ALL)


def get_max_temp(year, city):

    # Reading the data from the csv file.
    data = pd.read_csv('./' + city.lower() + '.csv')

    # Filter the data for the given year
    year_data = data[data['Time'].str.startswith(year)]

    if not year_data.empty:
        # highest temperature and corresponding day
        max_temp = year_data['Max TemperatureC'].max()
        max_temp_day = year_data.loc[year_data['Max TemperatureC']
                                     == max_temp, 'Time'].values[0]

        # lowest temperature and corresponding day
        min_temp = year_data['Min TemperatureC'].min()
        min_temp_day = year_data.loc[year_data['Min TemperatureC']
                                     == min_temp, 'Time'].values[0]

        # most humid day and humidity
        max_humidity = year_data['Max Humidity'].max()
        max_humidity_day = year_data.loc[year_data['Max Humidity']
                                         == max_humidity, 'Time'].values[0]
        max_humidity_value = year_data.loc[year_data['Max Humidity']
                                           == max_humidity, 'Max Humidity'].values[0]

        # convert day format
        max_humidity_day = pd.to_datetime(max_humidity_day).strftime('%d %B')
        max_temp_day = pd.to_datetime(max_temp_day).strftime('%d %B')
        min_temp_day = pd.to_datetime(min_temp_day).strftime('%d %B')

        display_max_min_temp(year, max_temp, max_temp_day, min_temp,
                             min_temp_day, max_humidity_day, max_humidity_value)
    else:
        print("No data available for the year", year)


def get_monthly_avg(year, month, city):
    # Read the data from the CSV file
    data = pd.read_csv('./' + city.lower() + '.csv')

    data.dropna()

    # Filter the data for the given year
    year_data = data[data['Time'].str.startswith(year)]

    if not year_data.empty:
        # Filter the data for the given month
        month_data = year_data[year_data['Time'].str.contains(
            year + '-' + month)]

        # month_data.to_csv('./before_' + city.lower() + '_' +
        #                   year + '_' + month + '.csv')

        # drow rows with NaN values in max temp, min temp, mean humidity
        month_data = month_data[month_data['Max TemperatureC'].notna()]
        month_data = month_data[month_data['Min TemperatureC'].notna()]
        month_data = month_data[month_data[' Mean Humidity'].notna()]

        # write month data to a csv file
        # month_data.to_csv('./' + city.lower() + '_' +
        #                   year + '_' + month + '.csv')
        # print(month_data.head())

        if not month_data.empty:
            # average highest temperature
            avg_max_temp = month_data['Max TemperatureC'].mean()

            # average lowest temperature
            avg_min_temp = month_data['Min TemperatureC'].mean()

            # average humidity
            avg_humidity = month_data[' Mean Humidity'].mean()

            display_monthly_avg_temp(
                year, month, avg_max_temp, avg_min_temp, avg_humidity)
        else:
            print("No data available for the month", month + '/' + year)
    else:
        print("No data available for the year", year)


def get_daily_max_min(year, month, city):
    # Read the data from the CSV file
    data = pd.read_csv('./' + city.lower() + '.csv')

    data.dropna()

    # Filter the data for the given year
    year_data = data[data['Time'].str.startswith(year)]

    if not year_data.empty:
        # Filter the data for the given month
        month_data = year_data[year_data['Time'].str.contains(
            year + '-' + month + '-')]

        # drow rows with NaN values in max temp, min temp, mean humidity
        month_data = month_data[month_data['Max TemperatureC'].notna()]
        month_data = month_data[month_data['Min TemperatureC'].notna()]

        if not month_data.empty:
            # Extract the relevant columns
            days = month_data['Time']
            # reformat days
            days = pd.to_datetime(days).dt.strftime('%d %B')

            max_temps = month_data['Max TemperatureC']
            min_temps = month_data['Min TemperatureC']

            # Create the figure and axes
            fig, ax = plt.subplots()

            # Plot the highest temperatures as horizontal bars in red
            ax.barh(days, max_temps, color='red', label='Highest Temperature')

            # Plot the lowest temperatures as horizontal bars in blue
            ax.barh(days, min_temps, color='blue', label='Lowest Temperature')

            # Set the y-axis labels
            ax.set_yticklabels(days)

            # Set the title and labels
            ax.set_title("Highest and Lowest Temperatures for the Month")
            ax.set_xlabel("Temperature (°C)")
            ax.set_ylabel("Day")

            # Display the legend
            ax.legend()

            ax.figure.set_size_inches(10, 10)

            # Show the plot
            plt.show()
    else:
        print("No data available for the year", year)


def get_daily_max_min_no_Graph(year, month, city):
    # Read the data from the CSV
    data = pd.read_csv('./' + city.lower() + '.csv')

    data.dropna()

    # Filter the data for the given year
    year_data = data[data['Time'].str.startswith(year)]

    if not year_data.empty:
        # Filter the data for the given month
        month_data = year_data[year_data['Time'].str.contains(
            year + '-' + month + '-')]

        # month_data.to_csv('./before_' + city.lower() + '_' + month + '.csv')

        # drow rows with NaN values in max temp, min temp, mean humidity
        month_data = month_data[month_data['Max TemperatureC'].notna()]
        month_data = month_data[month_data['Min TemperatureC'].notna()]

        month_data = month_data.reset_index(drop=True)

        # month_data.to_csv('./' + city.lower() + '_' + month + '.csv')

        if not month_data.empty:

            # Extract the relevant columns
            days = month_data['Time']
            # print(days)
            # reformat days
            days = pd.to_datetime(days).dt.strftime('%d %B')

            max_temps = month_data['Max TemperatureC']
            min_temps = month_data['Min TemperatureC']

        display_daily_max_min_temp(days, max_temps, min_temps)
    else:
        print("No data available for the year", year)


def get_daily_max_min_single(year, month, city):
    # Read the data from the CSV
    data = pd.read_csv('./' + city.lower() + '.csv')

    data.dropna()

    # Filter the data for the given year
    year_data = data[data['Time'].str.startswith(year)]

    if not year_data.empty:
        # Filter the data for the given month
        month_data = year_data[year_data['Time'].str.contains(
            year + '-' + month + '-')]

        # month_data.to_csv('./before' + city.lower() + '_' + month + '.csv')

        # drow rows with NaN values in max temp, min temp, mean humidity
        month_data = month_data[month_data['Max TemperatureC'].notna()]
        month_data = month_data[month_data['Min TemperatureC'].notna()]

        month_data = month_data.reset_index(drop=True)

        # month_data.to_csv('./' + city.lower() + '_' + month + '.csv')

        if not month_data.empty:
            # Extract the relevant columns
            days = month_data['Time']
            # reformat days
            days = pd.to_datetime(days).dt.strftime('%d %B')

            max_temps = month_data['Max TemperatureC']
            min_temps = month_data['Min TemperatureC']

        display_daily_max_min_temp_single(days, max_temps, min_temps)
    else:
        print("No data available for the year", year)
