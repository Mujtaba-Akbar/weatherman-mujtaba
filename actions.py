import argparse
from weather_data_parser import WeatherDataParser
from calculator import Calculator
from report_generator import ReportGenerator


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
