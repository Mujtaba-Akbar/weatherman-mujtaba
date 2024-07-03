import argparse
import os
import sys
import math
from collections import namedtuple
from datetime import datetime


# consts for indexes in WeatherReading tuple
DATE_INDEX = 0
MAX_TEMP_INDEX = 1
MEAN_TEMP_INDEX = 2
MIN_TEMP_INDEX = 3
MAX_HUMIDITY_INDEX = 4
MEAN_HUMIDITY_INDEX = 5
MIN_HUMIDITY_INDEX = 6

# ansi color codes
RED_COLOR = '\033[91m'
BLUE_COLOR = '\033[94m'
RESET_COLOR = '\033[0m'

# data structure to hold weather readings for a given day
WeatherReading = namedtuple('WeatherReading', [
    'date', 'max_temp', 'mean_temp', 'min_temp', 'max_humidity', 'mean_humidity', 'min_humidity'
])


class DictDataItem(dict):
    ''' Dictionary data item to store key value pairs '''

    def __init__(self, *args, **kwargs):
        ''' Initialize the dictionary data item

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        '''
        super().__init__(*args, **kwargs)

    def add_data(self, key, value):
        ''' Add data to the dictionary

        Args:
            key (str): The key
            value (str): The value
        '''
        self[key] = value

    def get_data(self, key):
        ''' Get data from the dictionary

        Args:
            key (str): The key
        Returns:
            str: The value'''
        return self.get(key)

    def __str__(self):
        ''' Convert the dictionary to a string

        Returns:
            str: The string representation of the dictionary
        '''
        return str(dict(self))


class WeatherDataParser:
    ''' Parser class which populates the data rows '''

    def __init__(self, folder_path):
        ''' Initialize the WeatherDataParser

        Args:
            folder_path (str): The folder path

            '''
        self.weather_readings = []
        self.folder_path = folder_path

    def parse_float(self, value):
        ''' Parse a float value

        Args:
            value (str): The value to parse
        Returns:
            float: The parsed float value
        '''
        try:
            return float(value)
        except ValueError:
            return float('nan')

    def populate_data(self):
        ''' Populate the data from the files

        Returns:
            list: The list of WeatherReading objects

        '''
        # get list of files in the folder
        files = os.listdir(self.folder_path)
        for file in files:
            with open(os.path.join(self.folder_path, file), "r") as f:
                for line in f.readlines()[1:]:
                    entry = line.strip().split(',')
                    if entry:
                        # create a WeatherReading object and append to list
                        self.weather_readings.append(WeatherReading(
                            entry[DATE_INDEX],
                            self.parse_float(entry[MAX_TEMP_INDEX]),
                            self.parse_float(entry[MEAN_TEMP_INDEX]),
                            self.parse_float(entry[MIN_TEMP_INDEX]),
                            self.parse_float(entry[MAX_HUMIDITY_INDEX+3]),
                            self.parse_float(entry[MEAN_HUMIDITY_INDEX+3]),
                            self.parse_float(entry[MIN_HUMIDITY_INDEX+3])
                        ))

        return self.weather_readings


class Calculator:
    ''' Class to calculate extremes, averages for a given year or month 
    '''

    def __init__(self, weather_readings: WeatherReading):
        ''' Initialize the calculator with the weather readings

        Args:
            weather_readings (list): The list of weather readings

        '''
        self.weather_readings = weather_readings
        self.calculation_results = DictDataItem()

    def filter_readings(self, readings, year=None, month=None):
        ''' Filter readings based on year and month

        Args:
            readings (list): The list of readings
            year (int): The year
            month (int): The month
        Returns:
            list: The filtered list of readings
        '''

        def matches_criteria(reading):
            date_obj = datetime.strptime(reading.date, '%Y-%m-%d')
            if year is not None and date_obj.year != year:
                return False
            if month is not None and date_obj.month != month:
                return False
            return True

        return [reading for reading in readings if matches_criteria(reading)]

    def find_extremes_for_year(self, year):
        ''' Find the extremes for the given year

        Args:
            year (int): The year
        Returns:
            DictDataItem: The calculation results
        '''
        # filter readings for the given year
        filtered_readings = self.filter_readings(
            self.weather_readings, year=int(year))

        if not filtered_readings:
            return "No data available for this year."

        # find the max, min temperature reading and max humidity reading
        max_temp_reading = None
        min_temp_reading = None
        max_humidity_reading = None

        for reading in filtered_readings:
            if not math.isnan(reading.max_temp):
                if max_temp_reading is None or reading.max_temp > max_temp_reading.max_temp:
                    max_temp_reading = reading
            if not math.isnan(reading.min_temp):
                if min_temp_reading is None or reading.min_temp < min_temp_reading.min_temp:
                    min_temp_reading = reading
            if not math.isnan(reading.max_humidity):
                if max_humidity_reading is None or reading.max_humidity > max_humidity_reading.max_humidity:
                    max_humidity_reading = reading
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
            'max_humidity', max_humidity_reading.max_humidity)
        self.calculation_results.add_data(
            'max_humidity_date', max_humidity_reading.date)

        return self.calculation_results

    def calculate_month_averages(self, year, month):
        ''' Calculate the averages for the given month

        Args:
            year (int): The year
            month (int): The month
        Returns:
            DictDataItem: The calculation results
        '''

        filtered_readings = self.filter_readings(
            self.weather_readings, year=year, month=month)

        if not filtered_readings:
            return "No data available for this year."

        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0
        max_temp_count = 0
        min_temp_count = 0
        mean_humidity_count = 0

        for reading in filtered_readings:
            if not math.isnan(reading.max_temp):
                total_max_temp += float(reading.max_temp)
                max_temp_count += 1
            if not math.isnan(reading.min_temp):
                total_min_temp += float(reading.min_temp)
                min_temp_count += 1
            if not math.isnan(reading.mean_humidity):
                total_mean_humidity += float(reading.mean_humidity)
                mean_humidity_count += 1

            average_max_temp = round(
                total_max_temp / max_temp_count, 2) if max_temp_count > 0 else float('nan')
            average_min_temp = round(
                total_min_temp / min_temp_count, 2) if min_temp_count > 0 else float('nan')
            average_mean_humidity = round(
                total_mean_humidity / mean_humidity_count, 2) if mean_humidity_count > 0 else float('nan')

            self.calculation_results.add_data('avg_lowest_temp',
                                              average_min_temp)
            self.calculation_results.add_data('avg_highest_temp',
                                              average_max_temp)
            self.calculation_results.add_data('avg_mean_humidity',
                                              average_mean_humidity)
        return self.calculation_results

    def populate_temp_extremes_for_month(self, year, month):
        ''' Populate the temperature extremes for the given month

        Args:
            year (int): The year
            month (int): The month
        Returns:
            DictDataItem: The calculation results

            '''

        # filter readings for the given month
        filtered_readings = self.filter_readings(
            self.weather_readings, year=year, month=month)
        if not filtered_readings:
            return "No data available for this year and month."

        if filtered_readings:
            max_temps = []
            min_temps = []
            for reading in filtered_readings:
                if not math.isnan(reading.max_temp):
                    max_temps.append(reading.max_temp)
                if not math.isnan(reading.min_temp):
                    min_temps.append(reading.min_temp)
            # add data to the calculation results
            self.calculation_results.add_data('year', year)
            self.calculation_results.add_data('month', month)
            self.calculation_results.add_data('max_temps', max_temps)
            self.calculation_results.add_data('min_temps', min_temps)
            return self.calculation_results


class ReportGenerator():
    ''' Class to generate reports

    Attributes:
        result (DictDataItem): The calculation results
        months (List): List of month names

    '''

    def __init__(self, result: DictDataItem):
        ''' Initialize the report generator with the calculation results

        Args:
            result (DictDataItem): The calculation results

        '''

        if isinstance(result, str):
            print(result)
            sys.exit(1)

        self.result = result
        self.months = [
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December"
        ]

    def format_date(self, date):
        ''' Format the date in the format "Month Day"

        Args:
            date (str): The date in the format "YYYY-MM-DD"

            Returns:
                str: The formatted date in the format "Month Day"
        '''
        _, month_num, day = date.split("-")
        return f"{self.months[int(month_num) - 1]} {day}"

    def generate_year_extremes_report(self):
        ''' Generate a report string for the year's extremes

        Returns:
            str: The report string
        '''

        max_temp_month_day = self.format_date(
            self.result.get_data('max_temp_date'))
        min_temp_month_day = self.format_date(
            self.result.get_data('min_temp_date'))
        max_humidity_month_day = self.format_date(
            self.result.get_data('max_humidity_date'))
        report_string = f"Highest: {self.result.get_data('max_temp')}C on {
            max_temp_month_day}\n"
        report_string += f"Lowest: {self.result.get_data('min_temp')}C on {
            min_temp_month_day}\n"
        report_string += f"Humidity: {self.result.get_data('max_humidity')}% on {
            max_humidity_month_day}\n"

        return report_string

    def generate_month_avg_report(self):
        '''
        Generate a report string for the month's averages

        Returns:
            str: The report string
        '''
        # generating report string for month's averages
        report_string = (f"Avg Lowest Temp: {self.result.get_data("avg_lowest_temp"):.2f}C\n"
                         f"Avg Highest Temp: {self.result.get_data(
                             "avg_highest_temp"):.2f}C\n"
                         f"Avg Mean Humidity: {self.result.get_data("avg_mean_humidity"):.2f}%\n")

        return report_string

    def print_month_extremes_bar_chart(self):
        ''' Print a bar chart for the month's temperature extremes
        '''

        # adjust for zero-based index
        print(f"{self.months[self.result.get_data('month')-1]} {
            self.result.get_data('year')}")

        for day, (max_temp, min_temp) in enumerate(zip(
                self.result.get_data('max_temps'), self.result.get_data('min_temps')), start=1):

           # generate bar for max temp in red
            max_bar = RED_COLOR + '+' * \
                int(max_temp) + RESET_COLOR + f" {int(max_temp)}C"

    # generate bar for min temp in blue
            min_bar = BLUE_COLOR + '+' * \
                int(min_temp) + RESET_COLOR + f" {int(min_temp)}C"
            print(f"{day:02} {max_bar}")
            print(f"{day:02} {min_bar}")

        print("\n")

    def print_net_month_extremes_bar_chart(self):
        ''' Print a bar chart for the month's net temperature extremes
        '''
        # prints a bar chart for month's net extremes
        for day, (max_temp, min_temp) in enumerate(
            zip(self.result.get_data('max_temps'),
                self.result.get_data('min_temps')),
            start=1
        ):
            net_bar = (
                BLUE_COLOR + '+' * int(min_temp) + RESET_COLOR +
                RED_COLOR + '+' * int(max_temp - min_temp) + RESET_COLOR +
                f" {int(min_temp):02}C - {int(max_temp):02}C"
            )
            print(f"{day:02} {net_bar}")


class YearlyExtremesAction(argparse.Action):
    ''' Generate yearly extremes report 

    Attributes:
        data_dir (str): The path to the data files

        '''

    def __call__(self, parser, namespace, values, option_string=None):
        year = values

        parser = WeatherDataParser(namespace.data_dir)
        weather_data = parser.populate_data()
        calculator = Calculator(weather_data)
        calculations_results = calculator.find_extremes_for_year(year)
        report = ReportGenerator(calculations_results)
        print(report.generate_year_extremes_report())


class MonthlyAveragesAction(argparse.Action):
    ''' Generate monthly averages report 

    Attributes:
        data_dir (str): The path to the data files
        '''

    def __call__(self, parser, namespace, values, option_string=None):
        ''' Generate monthly averages report

        Args:
            parser (argparse.ArgumentParser): The parser object
            namespace (argparse.Namespace): The namespace object
            values (str): The values for the month
            option_string (str): The option string
        '''
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
    ''' Generate basic barchart for daywise temperatures 

    Attributes:
        data_dir (str): The path to the data files

    '''

    def __call__(self, parser, namespace, values, option_string=None):
        ''' Generate basic barchart for daywise temperatures

        Args:
            parser (argparse.ArgumentParser): The parser object
            namespace (argparse.Namespace): The namespace object
            values (str): The values for the month
            option_string (str): The option string
        '''
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
    ''' Generate net effect bar charts for eachday

    Attributes:
        data_dir (str): The path to the data files
    '''

    def __call__(self, parser, namespace, values, option_string=None):
        '''
        Generate net effect bar charts for each day

        Args:
            parser (argparse.ArgumentParser): The parser object
            namespace (argparse.Namespace): The namespace object
            values (str): The values for the month
            option_string (str): The option string

        '''
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


def create_parser():
    ''' Create a parser object

    Returns:
        argparse.ArgumentParser: The parser object'''
    def validate_year(value):
        ''' Validate the year format
        Args:
            value (str): The year value
        Returns:
            str: The year value
                '''
        try:
            datetime.strptime(value, "%Y")
            return value
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid year format: {value}. Expected format: YYYY")

    def validate_year_month(value):
        ''' Validate the year/month format
        Args:
            value (str): The year/month value
        Returns:
            str: The year/month value
        '''
        try:
            datetime.strptime(value, "%Y/%m")
            return value
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid year/month format: {value}. Expected format: YYYY/MM")

    parser = argparse.ArgumentParser(description="Weatherman")
    parser.add_argument("data_dir", type=str,
                        help="Path to data files")
    parser.add_argument("-e", "--year", type=validate_year,
                        action=YearlyExtremesAction, help="Yearly extremes report")
    parser.add_argument("-a", "--month", type=validate_year_month,  action=MonthlyAveragesAction,
                        help="Month in format YYYY/MM for averages report")
    parser.add_argument("-c", "--chart",

                        action=NetChartAction, help="Month in format YYYY/MM for for barcharts")
    return parser


def main():
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parser.parse_args()


if __name__ == "__main__":
    main()
