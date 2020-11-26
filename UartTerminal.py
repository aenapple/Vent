import serial
import sys
import time


class UartTerminal(object):
    def __init__(self):
        self.index_print = 0
        self.ComPort = None

    def open(self, com_port, baud_rate):
        # com_port = 'COM3'
        # baud_rate = 115200
        try:
            self.ComPort = serial.Serial(com_port, baud_rate, timeout=0.1)
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
        time.sleep(0.1)
        read_line1 = self.ComPort.readline()
        len_data = len(read_line1)
        # print(read_line1)
        # print(len_data)
        if len_data == 0:  #
            return 1, 'No main board'

        try:
            x = read_line1.decode().find("tx OK")
            if x == 0:
                read_line2 = self.ComPort.readline()
                # return_str = read_line2.decode()

                len_data = len(read_line2)
                if len_data == 0:
                    return 1, 'No module - ' + str(number_module)
                else:
                    return 0, read_line2.decode()
            else:
                return 2, 'ERROR'
        except serial.SerialException:
            print("Serial Exception:")
            print(sys.exc_info())
            return 2, 'ERROR'