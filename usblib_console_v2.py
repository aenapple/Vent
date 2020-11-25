import usb
import ctypes
import array
import getopt
import sys
import time
import msvcrt


class DeviceException(BaseException):
    pass

def GetMyDevices():
    busses = usb.busses()
    found = []
    for bus in busses:
        devices = bus.devices
        for device in devices:
            if device.idVendor == 0x155d and device.idProduct == 0xa004:
                found.append(device)
            #for Xilinx PID VID CDC
            elif device.idVendor == 0x03FD and device.idProduct == 0x0100:
                found.append(device)
            elif device.idVendor == 0x0BED and device.idProduct == 0x0900:
                found.append(device)
            elif device.idVendor == 0x0BED and device.idProduct == 0x0601:
                found.append(device)
    if not found:
        raise DeviceException("Device not found!")
    return found
    
def SelectByProductString(devices, product):
    for device in devices:
        handle = device.open()
        #Manufacturer = handle.getString(device.iManufacturer, 255)
        Product = handle.getString(device.iProduct, 255)
        #print Product
        #SerialNumber = handle.getString(device.iSerialNumber, 255)
        if product == Product:
            return device

class LXB(object):
    def __init__(self, device):
        handle = device.open()
        #print dir(device)
        print dir(handle)
        print dir(handle.dev)
        interface = device.configurations[0].interfaces[0][1]
        handle.setConfiguration(1)
        handle.claimInterface(interface.interfaceNumber)
        self.handle = handle
        self.interface = interface
        for endp in self.interface.endpoints:
            print endp
            if endp.address & 0x80:
                self.endin = endp
                print 'IN set to ', hex(endp.address)
                print dir(endp)
                print endp.maxPacketSize
            else:
                self.endout = endp
                print 'OUT set to ', hex(endp.address)
        #print dir(self.handle)
        #print dir(self.endin)
        
    def Write(self, data, timeout=100):
        return self.handle.bulkWrite(self.endout.address, data, timeout)
        
    def Read(self, count=None, timeout=100):
        try:
            return self.handle.bulkRead(self.endin.address, count or self.endin.maxPacketSize, timeout)
        except:
            pass
            
            
class scanif_comn_frame(ctypes.Structure):
    _pack_ = 1
    _fields_ = [ ("MsgId", ctypes.c_uint16),
                 ("Addr", ctypes.c_uint32),
                 ("Size", ctypes.c_uint32),
                 ("Flag", ctypes.c_int16),
                 ("Reserved", ctypes.c_uint16),
                 ("FCS", ctypes.c_uint16),
                 ]
    def __init__(self, id, addr=0, size=0, flag=0):
        self.MsgId = id
        self.Addr = addr
        self.Size = size
        self.Flag = flag
        self.sign()
        
    def sign(self):
        self.FCS = CalcCRC16(0, self, 14)
        
    def to_binstr(self):
        return ctypes.cast(ctypes.pointer(self), ctypes.POINTER(ctypes.c_char))[:ctypes.sizeof(self)]
    
    def to_array(self):
        return array.array('B', self.to_binstr())
        
    def __str__(self):
        frmt = 'MsgId {self.MsgId:#x}, Addr {self.Addr:#x}, Size {self.Size}, Flag {self.Flag:#x}, FCS {self.FCS:#x}'
        return frmt.format(self=self)
        
    @staticmethod
    def from_binstr(bstring):
        return scanif_comn_frame.from_buffer_copy(bstring)

class ServerAck(scanif_comn_frame):
    def __init__(self):
        scanif_comn_frame.__init__(self, 0x11)
        
class ServerRequestData(scanif_comn_frame):
    def __init__(self, addr, size):
        scanif_comn_frame.__init__(self, 0x12, addr, size)

class ServerDone(scanif_comn_frame):
    def __init__(self):
        scanif_comn_frame.__init__(self, 0x13)

def CalcCRC16(InitCRC, Buf, Count):
    crc = InitCRC
    p = ctypes.cast(ctypes.pointer(Buf), ctypes.POINTER(ctypes.c_uint16))
    for i in xrange(0, Count/2):
        crc ^= p[i]
    
    #if (Count & 1)
    #    crc ^= *(unsigned char*)p
    return crc
    
class MyKeyboardEvent(object):
    def __init__(self, name, event_type):
        self.event_type = event_type
        self.name = name

class UIServer(object):
    def __init__(self, port):
        self.port = port
        self.collect = False
        self.command_buffer = ""
    
    def on_key(self, event):
        #print dir(event)
        #print event.device
        if event.event_type == 'down':
            if event.name == '\r':
                self.command_buffer += '\n'
                self.port.Write(self.command_buffer)
                if self.command_buffer.startswith("Log t") or self.command_buffer.startswith("Log d"):
                    self.collect_log()
                self.command_buffer = ""
                print 
            elif event.name == '\b':
                self.command_buffer = self.command_buffer[:-1]
            else:
                self.command_buffer += event.name
            sys.stdout.write(event.name)
            
    def collect_log(self):
        timeout = time.time() + 1.0
        data = ""
        while True:
            r = self.port.Read(512*16*2)
            if r:
                timeout = time.time() + 1.0
                data += r.tostring()
            else:
                if time.time() > timeout:
                    break
        with open('EventLog.bin', 'wb') as f:
            f.write(data)
        fname = 'EventLog%s.bin' % time.ctime().replace(':', '-')
        with open(fname, 'wb') as f:
            f.write(data)
    
    def serv(self, use_global_hooks=True):
        with open('console %s.txt' % time.ctime().replace(':', '-'), 'a') as txt:
            l = "session started at " + time.asctime()
            print l
            txt.write(l)
            txt.write('\n')
            while True:
                r = self.port.Read()
                if r:
                    s = r.tostring()
                    print s,
                    txt.write(s)
                    if len(s) == 1:
                        if ord(s) == 5:
                            self.port.Write('PuTTY')
                else:
                    GetMyDevices() # will create DeviceException
                    if not use_global_hooks:
                        if msvcrt.kbhit():
                            c = msvcrt.getch()
                            self.on_key(MyKeyboardEvent(c, 'down'))
                    if self.collect:
                        print "Saving log"
                        self.collect_log()
                        self.collect = False
                        print "Finished"
        
            


if __name__ == "__main__":
    __doc__ = """
Tool for receive and record from specified COM port in binary format
    Usage:
        --port= compatibility option
        --baudrate= compatibility option
        --append append to already existing file
        --use_global_hooks capture all keyboard events, even then window is not in focus
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hva", 
        ["help", "port=", 'baudrate=', 'append', 'use_global_hooks'])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    #default
    baudrate = 57600
    port = 'COM2'
    verbose = False
    gen_name = False
    use_global_hooks = False
    filemode = 'wb'
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        if o in ("--baudrate"):
            baudrate = int(a, 10)
        if o in ("--port"):
            port = a
        if o in ("--use_global_hooks"):
            use_global_hooks = True
        if o in ("-v"):
            verbose = True
        if o in ("-a", "--append"):
            filemode = 'a+b'
    msm_gx_product = "CDC ACM Driver"
    while True:
        try:
            device = SelectByProductString(GetMyDevices(), msm_gx_product)
            lxb = LXB(device)
            uiserv = UIServer(lxb)
            uiserv.serv(use_global_hooks)
        except DeviceException:
            lxb.handle.finalize()
            time.sleep(3)
        
            

    