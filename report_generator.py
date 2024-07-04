import sys
from dict_data_item import DictDataItem
from consts import RED_COLOR, BLUE_COLOR, RESET_COLOR


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

    def format_date(self, date: str):
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
