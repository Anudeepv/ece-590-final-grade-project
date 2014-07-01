#!/usr/bin/env python
import hubo_ach as ha
import ach
import sys
import time
from ctypes import *
import curses
import tty,termios
import os

class robotcontrol(object):

        
	#s=r=ref=state=None
        s = None
        r = None
        refParent = None
        state = None

	def __init__(self):
		#x=robotcontrol()
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		self.s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)	
		self.r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

		# feed-forward will now be refered to as "state"
		self.state = ha.HUBO_STATE()

		# feed-back will now be refered to as "ref"
		self.refParent = ha.HUBO_REF()

		# Get the current feed-forward (state) 
		[statuss, framesizes] = self.s.get(self.state, wait=False, last=False)

	        self.key()

	def key(self):
	    while(1):
                os.clear()
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
			self.back()
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
	

	def left(self):
	    #turning right

	    print "start"
	    print "turning."
	    self.refParent.ref[ha.WST] =  1
	    self.refParent.ref[ha.RHY] =  0.8
	    self.refParent.ref[ha.LHY] =  1
	    self.r.put(self.refParent)
	    time.sleep(20)
	    print "turning.."
	    self.refParent.ref[ha.WST] =  0.5
	    self.refParent.ref[ha.RHY] =  0.4
	    self.refParent.ref[ha.LHY] =  0.5
	    self.r.put(self.refParent)
	    time.sleep(20)	
		
	    print "Done R turning.."

	def right(self):
            #turning left
	    print "start"
	    print "turning."
	    self.refParent.ref[ha.WST] =  -1
	    self.refParent.ref[ha.LHY] =  -0.8
	    self.refParent.ref[ha.RHY] =  -1
	    self.r.put(self.refParent)
	    time.sleep(20)
	    print "turning.."
	    self.refParent.ref[ha.WST] =  -0.5
	    self.refParent.ref[ha.LHY] =  -0.4
	    self.refParent.ref[ha.RHY] =  -0.5
	    self.r.put(self.refParent)
	    time.sleep(20)	
			
	    print "Done L turning.."
	
	def stop(self):
	    #stop
	    print "stopping"	
	    print "stabilizing.."
	
	    self.refParent.ref[ha.RHY] = 0.0
	    self.refParent.ref[ha.LHY] = 0.0
	    self.refParent.ref[ha.LHP] = 0.0
	    self.refParent.ref[ha.LKN] = 0.0
	    self.refParent.ref[ha.RAP] = 0.0
	    self.refParent.ref[ha.RHP] = 0.0
	    self.refParent.ref[ha.RKN] = 0.0
	    self.refParent.ref[ha.LAP] = 0.0
		
	    self.r.put(self.refParent)
	    time.sleep(40)
	    print "done s"


	def straight(self):
	    #walking foward
	    print "start"
	    print "walking"
	    self.refParent.ref[ha.LHP] += -0.2
	    self.r.put(self.refParent)
	    time.sleep(10)
	    self.refParent.ref[ha.LKN] +=  0.2
	    self.r.put(self.refParent)
	    time.sleep(10)
	    self.refParent.ref[ha.RAP] += -0.1
	    self.r.put(self.refParent)
	    time.sleep(10)

	    self.refParent.ref[ha.RHP] += -0.2
	    self.r.put(self.refParent)
	    time.sleep(3)
	    self.refParent.ref[ha.RKN] +=  0.2
	    self.r.put(self.refParent)
	    time.sleep(4)
	    self.refParent.ref[ha.LAP] += -0.1
	    self.r.put(self.refParent)
	    time.sleep(50)
	
	    print "done f"
	
	def back(self):
	    #walking foward
	    print "start"
	    print "walking"
	    self.refParent.ref[ha.LHP] += 0.1
	    self.r.put(self.refParent)
	    time.sleep(3)
	    self.refParent.ref[ha.LKN] += -0.1
	    self.r.put(self.refParent)
	    time.sleep(4)
	    self.refParent.ref[ha.RAP] +=  0.05
	    self.r.put(self.refParent)
	    time.sleep(10)

	    self.refParent.ref[ha.RHP] +=  0.1
	    self.r.put(self.refParent)
	    time.sleep(3)
	    self.refParent.ref[ha.RKN] +=  -0.1
	    self.r.put(self.refParent)
	    time.sleep(4)
	    self.refParent.ref[ha.LAP] += 0.05
	    self.r.put(self.refParent)
	    time.sleep(30)	

	    print "done b"
	def Delay(self,t):
		t1=(time.localtime(time.time())[5])
		t2=t1 +1
		while((t2-t1) <t):
			t2=(time.localtime(time.time())[5])
			print "done"
		
if __name__ == "__main__":
    r = robotcontrol()



