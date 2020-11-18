import serial
import time


def transfer_log(fname):
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
                    break


def flush_console():
    timeout = time.time() + 1.0
    while True:
        data = com.read(512)
        if data:
            print data
            print len(data)
            timeout = time.time() + 1.0
        else:
            if time.time() > timeout:
                    break


if __name__ == '__main__':
    port = 'COM14'
    baudrate = 115200
    com = serial.Serial(port, baudrate, timeout=0.1)
    #  com.flush()
    print com.out_waiting
    print com.get_settings()
    print com.reset_output_buffer()
    # flush_console()
    # com.write('?\r\n')# disable log
    time.sleep(0.5)
    # flush_console()
    # transfer_log('EventLog.bin')
    # transfer_log('EventLog%s.bin' % time.ctime().replace(':', '-'))
    
