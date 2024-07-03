import math
from datetime import datetime
from dict_data_item import DictDataItem
from weather_data_parser import WeatherReading


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

    def filter_readings(self, readings: WeatherReading, year=None, month=None):
        ''' Filter readings based on year and month

        Args:
            readings (list): The list of readings
            year (int): The year
            month (int): The month
        Returns:
            list: The filtered list of readings
        '''

        def matches_criteria(reading: WeatherReading):
            date_obj = datetime.strptime(reading.date, '%Y-%m-%d')
            if year is not None and date_obj.year != year:
                return False
            if month is not None and date_obj.month != month:
                return False
            return True

        return [reading for reading in readings if matches_criteria(reading)]

    def find_extremes_for_year(self, year: str):
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

    def calculate_month_averages(self, year: str, month: str):
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

    def populate_temp_extremes_for_month(self, year: str, month: str):
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
