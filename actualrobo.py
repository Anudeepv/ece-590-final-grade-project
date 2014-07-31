import serial                     # we need to import the pySerial stuff to use\par
import ach
import sys
import time
from ctypes import *
import curses
import tty,termios

class robotcontrol(object):

    # important AX-12 constants
    AX_WRITE_DATA = 3
    AX_READ_DATA = 4

    s = serial.Serial()               # create a serial port object\par
    s.baudrate = 1000000              # baud rate, in bits/second\par
    s.port = "/dev/ttyUSB0"           # this is whatever port your are using\par
    s.open()

    # set register values\par
    def setReg(index,reg,values):
        length = 3 + len(values)
        checksum = 255-((index+length+AX_WRITE_DATA+reg+sum(values))%256)          
        s.write(chr(0xFF)+chr(0xFF)+chr(index)+chr(length)+chr(AX_WRITE_DATA)+chr(reg))
        for val in values:
            s.write(chr(val))
        s.write(chr(checksum))

    def getReg(index, regstart, rlength):
        s.flushInput()   
        checksum = 255 - ((6 + index + regstart + rlength)%256)
        s.write(chr(0xFF)+chr(0xFF)+chr(index)+chr(0x04)+chr(AX_READ_DATA)+chr(regstart)+chr(rlength)+chr(checksum))
        vals = list()
        s.read()   # 0xff
        s.read()   # 0xff
        s.read()   # ID
        length = ord(s.read()) - 1
        s.read()   # toss error   
        while length > 0:
            vals.append(ord(s.read()))
            length = length - 1
        if rlength == 1:
            return vals[0]
        return vals

    def __init__(self):
            self.key()

    def key(self):
        while(1):
        print "use arrow keys to control robot"
        print "UP arrow/Down Arrow/Left Arrow/Right Arrow"      
        print "hit q thrice to exit"
            
            fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        k=ch
            if k=='':
                continue
            if k=='\x1b[A':
                print "up"
                self.straight()
                self.stop()
                continue
            elif k=='\x1b[B':
                print "down"
                self.stop()
                continue
            elif k=='\x1b[C':
                print "right"
                self.right()
                self.stop()
                continue
            elif k=='\x1b[D':
                print "left"
                self.left()
                self.stop()
                continue
            elif k=='qqq':
                print "bye"
                break
            else:
                print "not an arrow key!"
    

    def right(self):
        #turning right

        print "start"
        print "turning."
        #self.refParent.ref[ha.LHY] =  1.2
        #self.r.put(self.refParent)
        setReg(7,30,(((670+69)%256),((670+69)>>8)))  
        self.Delay(5)
        print "turning.."
        #self.refParent.ref[ha.RHY] =  1.2
        #self.r.put(self.refParent)
        setReg(6,30,(((370+69)%256),((370+69)>>8)))
        self.Delay(40)  
        
        print "Done R turning.."

    def left(self):
            #turning left
        print "start"
        print "turning."
        #self.refParent.ref[ha.LHY] =  -1.2
        #self.r.put(self.refParent)
        setReg(7,30,(((670-69)%256),((670-69)>>8)))        
        self.Delay(5)
        print "turning.."
        #self.refParent.ref[ha.RHY] =  -1.2
        #self.r.put(self.refParent)
        setReg(7,30,(((670-69)%256),((670-69)>>8)))  
        self.Delay(60)  
            
        print "Done L turning.."
    
    def stop(self):
        #stop
        print "stopping"    
        print "stabilizing.."
    
        '''self.refParent.ref[ha.RHY] = 0.0
        self.refParent.ref[ha.LHY] = 0.0
        self.refParent.ref[ha.LHP] = 0.0
        self.refParent.ref[ha.LKN] = 0.0
        self.refParent.ref[ha.RAP] = 0.0
        self.refParent.ref[ha.RHP] = 0.0
        self.refParent.ref[ha.RKN] = 0.0
        self.refParent.ref[ha.LAP] = 0.0
    
        self.r.put(self.refParent)
    '''
        
        setReg(1,30,((512%256),(512>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(1,43,1)               # get the temperature\par

        setReg(2,30,((520%256),(520>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(2,43,1)               # get the temperature\par


        setReg(3,30,((512%256),(512>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(3,43,1)               # get the temperature\par


        setReg(4,30,((520%256),(520>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(4,30,2)               # get the temperature\par
        print getReg(4,31,2)

        setReg(5,30,((512%256),(512>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(5,43,1)               # get the temperature\par


        setReg(6,30,((370%256),(370>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(6,30,2)               # get the temperature\par
        print getReg(6,31,2)
    
        setReg(7,30,((670%256),(670>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(7,30,2)               # get the temperature\par
        print getReg(7,31,2)

        setReg(8,30,((512%256),(512>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(8,43,1)               # get the temperature\par


        setReg(9,30,((520%256),(520>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(9,43,1)               # get the temperature\par


        setReg(10,30,((512%256),(512>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(10,43,1)               # get the temperature\par


        setReg(11,30,((520%256),(520>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(11,43,1)               # get the temperature\par


        setReg(12,30,((512%256),(512>>8)))  # this will move servo 1 to centered position (512)\par
        print getReg(12,43,1)               # get the temperature\par


        self.Delay(40)
        print "done s"


    def straight(self):
        #walking foward
        print "start"
        print "walking"
        #self.refParent.ref[ha.LHP] += -0.2
        #self.r.put(self.refParent)
        setReg(9,30,(((520-12)%256),((520-12)>>8)))  
        self.Delay(10)
        #self.refParent.ref[ha.LKN] +=  0.2
        #self.r.put(self.refParent)
        setReg(10,30,(((512+12)%256),((512+12)>>8)))
        self.Delay(10)
        #self.refParent.ref[ha.RAP] += -0.1
        #self.r.put(self.refParent)
        setReg(2,30,(((520-6)%256),((520-6)>>8)))       
        self.Delay(10)

        #self.refParent.ref[ha.RHP] += -0.2
        #self.r.put(self.refParent)
        setReg(4,30,(((520-12)%256),((520-12)>>8)))  
        self.Delay(3)
        #self.refParent.ref[ha.RKN] +=  0.2
        #self.r.put(self.refParent)
        setReg(3,30,(((512+12)%256),((512+12)>>8)))
        self.Delay(4)
        #self.refParent.ref[ha.LAP] += -0.1
        #self.r.put(self.refParent)
        setReg(11,30,(((520-6)%256),((520-6)>>8)))
        self.Delay(50)
    
        print "done f"
        
    def Delay(self,t):
        t1=(time.localtime(time.time())[5])
        t2=t1 +1
        while((t2-t1) <t):
            t2=(time.localtime(time.time())[5])
            print "done"
        
if __name__ == "__main__":
    r = robotcontrol()
