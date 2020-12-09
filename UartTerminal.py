import serial
import sys
import time
from LogFile import LogFile


class UartTerminal(object):
    def __init__(self):
        self.index_print = 0
        self.ComPort = None

    def open(self, com_port, baud_rate):
        # com_port = 'COM3'
        # baud_rate = 115200
        try:
            self.ComPort = serial.Serial(com_port, baud_rate, timeout=0.5)
        except serial.SerialException:
            print("Serial Exception:")
            print(sys.exc_info())
            return 1
        print(self.ComPort.out_waiting)
        print(self.ComPort.get_settings())
        print(self.ComPort.reset_output_buffer())
        return 0

    def ping(self):
        self.ComPort.write(b'ping\r\n')
        time.sleep(0.1)
        # read_data = self.ComPort.read(100)
        read_data = self.ComPort.readline()
        len_data = len(read_data)
        # print(read_data)
        # print(len_data)
        if len_data == 0:
            return 1
        else:
            x = read_data.decode().find("ping OK")
            if x == 0:
                return 0
            else:
                return 2

    def read_module(self, number_module):
        str_temp = 'tx 1,' + hex(number_module) + ',temp\r\n'
        str_command = str_temp.replace('0x', '').encode()
        print(str_command)
        # return 1
        self.ComPort.write(str_command)  # send command to module
        # time.sleep(0.1)
        read_line1 = self.ComPort.readline()
        len_data = len(read_line1)
        # print(read_line1)
        # print(len_data)
        if len_data == 0:  #
            return 1, 'No main board'

        x = read_line1.decode().find("tx OK")
        if x >= 0:
            read_line2 = self.ComPort.readline()
            # r = read_line2.decode().find("CRC_ERR")
            try:
                len_data = len(read_line2)
                if len_data == 0:
                    return 1, 'No module - ' + str(number_module)
                else:
                    return 0, read_line2.decode()
            except:
                print("Decode Exception:")
                return 2, 'ERROR'
        else:
            return 2, 'ERROR'

    def read_all_module(self):
        # str_array = []

        self.ComPort.write('m\r\n'.encode())  # send command to module
        read_line1 = self.ComPort.readline()
        print(read_line1)
        if len(read_line1) == 0:  #
            return 1, 'No main board'

        x = read_line1.decode().find("m OK")
        k = 0
        if x >= 0:
            while True:
                read_line2 = self.ComPort.readline()
                if len(read_line2) == 0:  #
                    continue
                # str_array.append(read_line2)
                log_file = LogFile()
                log_file.write_record(read_line2)
                # print(read_line2)
                k = k + 1
                print(k)
                if k == 16:
                    break
            return 0, 'OK'
        else:
            return 2, 'ERROR'
