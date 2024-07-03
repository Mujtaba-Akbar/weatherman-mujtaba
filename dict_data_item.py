
class DictDataItem(dict):
    ''' Dictionary data item to store key value pairs '''

    def __init__(self, *args, **kwargs):
        ''' Initialize the dictionary data item

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        '''
        super().__init__(*args, **kwargs)

    def add_data(self, key: str, value: float):
        ''' Add data to the dictionary

        Args:
            key (str): The key
            value (str): The value
        '''
        self[key] = value

    def get_data(self, key: str):
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
