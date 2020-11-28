import time
import sys
from LogFile import LogFile
from UartTerminal import UartTerminal



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
    ....
    """

    # log_file = LogFile();
    # log_file.write_record();
    # uartTerminal = UartTerminal()
    # uartTerminal.read_module(11)
    # sys.exit(3)

    uartTerminal = UartTerminal()
    if uartTerminal.open('COM3', 115200) != 0:
        sys.exit(2)

    while True:
        result = uartTerminal.ping()
        if result != 0:
            print(result)
            time.sleep(0.5)
            continue

        while True:
            result_mb = uartTerminal.ping()
            print(result_mb)
            if result_mb != 0:  # no connection with main board
                break

            for x in range(1, 13):
                if (x != 3) and (x != 4) and (x != 6) and (x != 9) and (x != 11) and (x != 12):
                    continue

                time.sleep(1.0)
                result_module = uartTerminal.read_module(x)
                print(result_module)
                if result_module[0] == 0:
                    log_file = LogFile()
                    log_file.write_record(result_module[1])

            time.sleep(60.0)
