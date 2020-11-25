import serial
import time
import sys


class UartTerminal(object):
    def __init__(self):
        self.index_print = 0
        self.ComPort = None

    def open(self):
        com_port = 'COM3'
        baud_rate = 115200
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
        # self.ComPort.write('Log t\r\n')
        # print("Hello", self.index_print)
        self.index_print += 1


"""def transfer_log(fname):
    com.write('Log t\r\n')  # transfer log
    time.sleep(0.1)
    timeout = time.time() + 1.0
    with open(fname, 'wb') as f:
        while True:
            data = com.read(256)
            if data:
                timeout = time.time() + 1.0
                f.write(data)
            else:
                if time.time() > timeout:
                    break """


"""def flush_console():
    timeout = time.time() + 1.0
    while True:
        data = com.read(512)
        if data:
            print(data)
            print(len(data))
            timeout = time.time() + 1.0
        else:
            if time.time() > timeout:
                    break"""


if __name__ == '__main__':
    __doc__ = """
    Tool for receive and record from specified COM port in binary format
    """
    uartTerminal = UartTerminal()
    if uartTerminal.open() != 0:
        sys.exit(2)

    while True:
        # uartTerminal.read_module(1)
        result = uartTerminal.ping()
        if result != 0:
            print(result)
            time.sleep(0.5)
            continue

        while True:
            time.sleep(0.5)
            result = uartTerminal.ping()
            print(result)
            if result != 0:
                break
