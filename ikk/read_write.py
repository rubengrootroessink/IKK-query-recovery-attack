# Imports os library to read and write files from/to folders on the machine
import os

# Imports json library so that dictionaries can be structured in the JSON format while writing and so that JSON structured data can be put
#   in a dictionary while reading
import json

# Date/datetime is used to ensure datetime are expressed in an ISO format while writing
from datetime import date, datetime

# Class IO is used to interact with JSON structured results of different simulations
# Method save_to_file a dictionary containing the results of a simulation to a specific file/folder in the 'Results' folder
# Method read_from_file is used to read in results in the 'Results' folder
# Method json_serial is used by the save_to_file method to ensure datetime objects are structured in an ISO format
class IO:

    # Method save_to_file writes data (Python dictionary) to a file in the 'Results/{{ simulation_name }}' folder
    def save_to_file(self, simulation_name, file_name, data):
        file_path = os.path.join(os.getcwd(), "Results", simulation_name, file_name)
        with open(file_path, "w") as file:
            json.dump(data, file, default=self.json_serial)

    # Method read_from_file reads data from a file into a dictionary from the 'Results/{{ simulation_name }}' folder
    def read_from_file(self, simulation_name, file_name):
        file_path = os.path.join(os.getcwd(), "Results", simulation_name, file_name)
        print(file_path)
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

    # Helper function for the save_to_file method to ensure a datetime object is structured in an ISO format
    def json_serial(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s is not serializable" % type(obj))
