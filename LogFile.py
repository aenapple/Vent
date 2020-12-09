import time
import datetime
from datetime import date

class LogFile(object):
    # def __init__(self):
    #    self.file = None

    def __open(self):
        pass

    def write_record(self, record):
        datetime_object = datetime.datetime.now()
        print(datetime_object)
        today = datetime_object.strftime("%m/%d/%Y-%H:%M:%S.%f-")
        file_name = 'LogTemperature.txt'
        str_temp = record.decode()
        # full_record = today + record.replace('temp from '.encode(), '')
        full_record = today + str_temp.replace('temp from ', '')
        print(full_record)

        file_out = open(file_name, 'a')
        file_out.write(full_record)
        file_out.close()

