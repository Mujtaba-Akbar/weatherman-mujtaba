import os
from collections import namedtuple
from datetime import datetime
import argparse


# consts for indexes in WeatherReading tuple
DATE_INDEX = 0
MAX_TEMP_INDEX = 1
MEAN_TEMP_INDEX = 2
MIN_TEMP_INDEX = 3
MAX_HUMIDITY_INDEX = 4
MEAN_HUMIDITY_INDEX = 5
MIN_HUMIDITY_INDEX = 6

# data structure to hold weather readings for a given day
WeatherReading = namedtuple('WeatherReading', [
    'date', 'max_temp', 'mean_temp', 'min_temp', 'max_humidity', 'mean_humidity', 'min_humidity'
])


class DictDataItem:
    ''' Dictionary data item to store key value pairs '''

    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data[key]

    def __str__(self):
        return str(self.data)


class WeatherDataParser:
    ''' Parser class which populates the data rows '''

    def __init__(self, folder_path):
        self.weather_reading_list = []
        self.folder_path = folder_path

    def safe_float(self, value):
        try:
            return float(value)
        except ValueError:
            return 'NaN'

    def populate_data(self):
        # get list of files in the folder
        files = os.listdir(self.folder_path)
        for file in files:
            with open(f"{self.folder_path}/{file}", "r") as f:
                for line in f.readlines()[1:]:
                    entry = line.strip().split(',')
                    if entry:
                        # create a WeatherReading object and append to list
                        self.weather_reading_list.append(WeatherReading(
                            entry[DATE_INDEX],
                            self.safe_float(entry[MAX_TEMP_INDEX]),
                            self.safe_float(entry[MEAN_TEMP_INDEX]),
                            self.safe_float(entry[MIN_TEMP_INDEX]),
                            self.safe_float(entry[MAX_HUMIDITY_INDEX+3]),
                            self.safe_float(entry[MEAN_HUMIDITY_INDEX+3]),
                            self.safe_float(entry[MIN_HUMIDITY_INDEX+3])
                        ))

        return self.weather_reading_list


class Calculator:
    ''' Class to calculate extremes, averages for a given year or month '''

    def __init__(self, weather_reading_list: WeatherReading):
        self.weather_reading_list = weather_reading_list
        self.calculation_results = DictDataItem()

    def find_extremes_for_year(self, year):

        # filter readings for the given year
        year_readings = [
            reading for reading in self.weather_reading_list if reading.date.startswith(str(year))]

        if year_readings:
            # find the max, min temperature reading and max humidity reading
            max_temp_reading = max(
                year_readings, key=lambda x: x.max_temp if x.max_temp != 'NaN' else float('-inf'))
            min_temp_reading = min(
                year_readings, key=lambda x: x.min_temp if x.min_temp != 'NaN' else float('inf'))
            max_humidity_rating = max(
                year_readings, key=lambda x: x.max_humidity if x.max_humidity != 'NaN' else float('-inf'))
            self.calculation_results.add_data('year', year)
            self.calculation_results.add_data(
                'max_temp', max_temp_reading.max_temp)
            self.calculation_results.add_data(
                'max_temp_date', max_temp_reading.date)
            self.calculation_results.add_data(
                'min_temp', min_temp_reading.min_temp)
            self.calculation_results.add_data(
                'min_temp_date', min_temp_reading.date)
            self.calculation_results.add_data(
                'max_humidity', max_humidity_rating.max_humidity)
            self.calculation_results.add_data(
                'max_humidity_date', max_humidity_rating.date)

            return self.calculation_results

        else:
            return "No data available for this year."

    def calculate_month_averages(self, year, month):
        filtered_readings = [
            reading for reading in self.weather_reading_list
            if datetime.strptime(reading.date, '%Y-%m-%d').year == year
            and datetime.strptime(reading.date, '%Y-%m-%d').month == month
        ]

    # compute averages
        if filtered_readings:
            total_max_temp = sum(float(reading.max_temp)
                                 for reading in filtered_readings if reading.max_temp != 'NaN')
            total_min_temp = sum(float(reading.min_temp)
                                 for reading in filtered_readings if reading.min_temp != 'NaN')
            total_mean_humidity = sum(float(reading.mean_humidity)
                                      for reading in filtered_readings if reading.mean_humidity != 'NaN')

            max_temp_count = len([
                reading for reading in filtered_readings if reading.max_temp != 'NaN'
            ])

            min_temp_count = len([
                reading for reading in filtered_readings if reading.min_temp != 'NaN'
            ])

            mean_humidity_count = len([
                reading for reading in filtered_readings if reading.mean_humidity != 'NaN'
            ])

            average_max_temp = round(total_max_temp / max_temp_count, 2)
            average_min_temp = round(total_min_temp / min_temp_count)
            average_mean_humidity = round(
                total_mean_humidity / mean_humidity_count)
        else:
            print("No data available for this month.")

        self.calculation_results.add_data('avg_lowest_temp',
                                          average_min_temp)
        self.calculation_results.add_data('avg_highest_temp',
                                          average_max_temp)
        self.calculation_results.add_data('avg_mean_humidity',
                                          average_mean_humidity)

        return self.calculation_results

    def populate_temp_extremes_for_month(self, year, month):
        # filter readings for the given month
        filtered_readings = [
            reading for reading in self.weather_reading_list
            if datetime.strptime(reading.date, '%Y-%m-%d').year == year
            and datetime.strptime(reading.date, '%Y-%m-%d').month == month
        ]

        if filtered_readings:
            max_temps = []
            min_temps = []
            for reading in filtered_readings:
                if reading.max_temp != 'NaN':
                    max_temps.append(reading.max_temp)
                if reading.min_temp != 'NaN':
                    min_temps.append(reading.min_temp)
            # add data to the calculation results
            self.calculation_results.add_data('year', year)
            self.calculation_results.add_data('month', month)
            self.calculation_results.add_data('max_temps', max_temps)
            self.calculation_results.add_data('min_temps', min_temps)
            return self.calculation_results


class ReportGenerator():
    ''' Class to generate reports '''

    def __init__(self, result: DictDataItem):
        self.result = result
        self.months = [
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December"
        ]

    def get_eng_date(self, date):
        _, month_num, day = date.split("-")
        return f"{self.months[int(month_num) - 1]} {day}"

    def generate_year_extremes_report(self):
        # generating report string for year's extremes

        max_temp_month_day = self.get_eng_date(
            self.result.get_data('max_temp_date'))
        min_temp_month_day = self.get_eng_date(
            self.result.get_data('min_temp_date'))
        max_humidity_month_day = self.get_eng_date(
            self.result.get_data('max_humidity_date'))
        report_string = f"Highest: {self.result.get_data('max_temp')}C on {
            max_temp_month_day}\n"
        report_string += f"Lowest: {self.result.get_data('min_temp')}C on {
            min_temp_month_day}\n"
        report_string += f"Humidity: {self.result.get_data('max_humidity')}% on {
            max_humidity_month_day}\n"

        return report_string

    def generate_month_avg_report(self):
        # generating report string for month's averages
        report_string = (f"Avg Lowest Temp: {self.result.get_data("avg_lowest_temp"):.2f}C\n"
                         f"Avg Highest Temp: {self.result.get_data(
                             "avg_highest_temp"):.2f}C\n"
                         f"Avg Mean Humidity: {self.result.get_data("avg_mean_humidity"):.2f}%\n")

        return report_string

    def print_month_extremes_bar_chart(self):

        # adjust for zero-based index
        print(f"{self.months[self.result.get_data('month')-1]} {
            self.result.get_data('year')}")

        for day, (max_temp, min_temp) in enumerate(zip(
                self.result.get_data('max_temps'), self.result.get_data('min_temps')), start=1):

            # gnerate bar for max temp in red
            max_bar = '\033[91m' + '+' * \
                int(max_temp) + "\033[0m" + f" {int(max_temp)}C"

            # generate bar for min temp in blue
            min_bar = '\033[94m' + '+' * \
                int(min_temp) + "\033[0m" f" {int(min_temp)}C\033[0m"

            print(f"{day:02} {max_bar}")
            print(f"{day:02} {min_bar}")

        print("\n")

    def print_net_month_extremes_bar_chart(self):
        # prints a bar chart for month's net extremes
        for day, (max_temp, min_temp) in enumerate(zip(
                self.result.get_data('max_temps'), self.result.get_data('min_temps')), start=1):
            net_bar = '\033[94m' + '+' * int(min_temp) + "\033[0m" + '\033[91m' + '+' * int(
                max_temp-min_temp) + "\033[0m" + f" {int(min_temp):02}C - {int(max_temp):02}C"
            print(f"{day:02} {net_bar}")


class YearlyExtremesAction(argparse.Action):
    ''' Generate yearly extremes report '''

    def __call__(self, parser, namespace, values, option_string=None):
        year = values

        parser = WeatherDataParser(namespace.data_dir)
        weather_data = parser.populate_data()
        calculator = Calculator(weather_data)
        calculations_results = calculator.find_extremes_for_year(year)
        report = ReportGenerator(calculations_results)
        print(report.generate_year_extremes_report())


class MonthlyAveragesAction(argparse.Action):
    ''' Generate monthly averages report '''

    def __call__(self, parser, namespace, values, option_string=None):
        year, month = values.split("/")
        year = int(year)
        month = int(month)

        parser = WeatherDataParser(namespace.data_dir)
        weather_data = parser.populate_data()
        calculator = Calculator(weather_data)
        calculation_results = calculator.calculate_month_averages(year, month)
        report = ReportGenerator(calculation_results)
        print(report.generate_month_avg_report())


class BasicChartAction(argparse.Action):
    ''' Generate basic barchart for daywise temperatures '''

    def __call__(self, parser, namespace, values, option_string=None):
        year, month = values.split("/")
        year = int(year)
        month = int(month)

        parser = WeatherDataParser(namespace.data_dir)
        weather_data = parser.populate_data()
        calculator = Calculator(weather_data)
        calculation_results = calculator.populate_temp_extremes_for_month(
            year, month)
        report = ReportGenerator(calculation_results)
        report.print_month_extremes_bar_chart()


class NetChartAction(argparse.Action):
    ''' Generate net effect bar charts for eachday'''

    def __call__(self, parser, namespace, values, option_string=None):
        year, month = values.split("/")
        year = int(year)
        month = int(month)

        parser = WeatherDataParser(namespace.data_dir)
        weather_data = parser.populate_data()
        calculator = Calculator(weather_data)
        calculation_results = calculator.populate_temp_extremes_for_month(
            year, month)
        report = ReportGenerator(calculation_results)
        report.print_net_month_extremes_bar_chart()


def main():
    parser = argparse.ArgumentParser(description="Weatherman")
    parser.add_argument("data_dir", type=str,
                        help="Path to data files")
    parser.add_argument("-e", "--year",
                        action=YearlyExtremesAction, help="Yearly extremes report")
    parser.add_argument("-a", "--month",  action=MonthlyAveragesAction,
                        help="Month in format YYYY/MM for averages report")
    parser.add_argument("-c", "--chart",
                        action=NetChartAction, help="Month in format YYYY/MM for for barcharts")
    parser.parse_args()


if __name__ == "__main__":
    main()
