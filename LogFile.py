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
        file_name = 'LogTemperature_' + record[0] + '.txt'
        full_record = today + record.replace(record[0] + ',1,temp OK ,', '')
        print(full_record)

        file_out = open(file_name, 'a')
        file_out.write(full_record)
        file_out.close()

