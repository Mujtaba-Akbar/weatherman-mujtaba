import argparse
from datetime import datetime
from actions import *


def create_parser():
    ''' Create a parser object

    Returns:
        argparse.ArgumentParser: The parser object'''
    def validate_year(value: str):
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

    def validate_year_month(value: str):
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
