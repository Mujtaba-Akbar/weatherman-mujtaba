import os
from collections import namedtuple
from consts import *


# data structure to hold weather readings for a given day
WeatherReading = namedtuple('WeatherReading', [
    'date', 'max_temp', 'mean_temp', 'min_temp', 'max_humidity', 'mean_humidity', 'min_humidity'
])


class WeatherDataParser:
    ''' Parser class which populates the data rows '''

    def __init__(self, folder_path: str):
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
