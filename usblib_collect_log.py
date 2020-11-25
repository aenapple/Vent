import usb
import ctypes
import array
import getopt
import sys
import time

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


class UIServer(object):
    def __init__(self, port):
        self.port = port
    
    def serv(self):
        while True:
            r = self.port.Read()
            if r:
                print r.tostring()
            else:
                break
        self.port.Write("e")
        time.sleep(0.3)
        while True:
            r = self.port.Read()
            if r:
                print r.tostring()
            else:
                break
        self.port.Write("t")
        timeout = time.time() + 1.0
        data = ""
        while True:
            r = self.port.Read()
            if r:
                timeout = time.time() + 1.0
                data += r.tostring()
            else:
                if time.time() > timeout:
                    break
        with open('EventLog.bin', 'wb') as f:
            f.write(data)
        self.port.Write("t")
        timeout = time.time() + 1.0
        data = ""
        while True:
            r = self.port.Read()
            if r:
                timeout = time.time() + 1.0
                data += r.tostring()
            else:
                if time.time() > timeout:
                    break
        fname = 'EventLog%s.bin' % time.ctime().replace(':', '-')
        with open(fname, 'wb') as f:
            f.write(data)
        
            


if __name__ == "__main__":
    __doc__ = """
Tool for receive and record from specified COM port in binary format
    Usage:
        --port= compatibility option
        --baudrate= compatibility option
        --generate-names to auto increment file name on next start
                record*.bin
        --append append to already existing file
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hva", 
        ["help", "port=", 'baudrate=', 'generate-names' , 'append'])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    #default
    baudrate = 57600
    port = 'COM2'
    verbose = False
    gen_name = False
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
        if o in ("--generate-names"):
            gen_name = True
        if o in ("-v"):
            verbose = True
        if o in ("-a", "--append"):
            filemode = 'a+b'
    msm_gx_product = "CDC ACM Driver"
    device = SelectByProductString(GetMyDevices(), msm_gx_product)
    lxb = LXB(device)
    uiserv = UIServer(lxb)
    from msvcrt import getch
    #getch()
    #uiserv.port.Write("hello")
    #while(1):
    #    print uiserv.port.Read()
    
    uiserv.serv()

    