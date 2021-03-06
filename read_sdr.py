from collections import deque
import numpy as numpy
from rtlsdr import *
from pylab import *
from scipy import signal
import time
from process_signal import process_packet

sdr = RtlSdr()
#sdr = RtlSdrTcpClient(hostname='localhost', port=1234)

# configure device
fs=2400000
sdr.sample_rate = 2400000
sdr.center_freq = 912200000

data_buffer=deque(maxlen=16384*4)

data_for_export=[]
counter=0
detect=False
while 1:
	read_data=sdr.read_samples(2048*4)
	data_buffer.extend(read_data)
	processed_data=np.absolute(np.asarray(data_buffer))
	edge_detect=signal.convolve(processed_data, [-1,-1,-1,-1,-1,0,1,1,1,1,1], mode='full', method='auto')
	maxx=np.amax(edge_detect)
	if maxx > 0.75:
		if detect == False:
			counter=0
		else:
			counter += 1
		detect=True
	if detect == True and counter == 6:
		detect = False
		print("Got Packet"+str(time.time()))
		#plot(processed_data)
		#show()
		try:
			process_packet(processed_data)
		except:
			pass
	#print(maxx, detect,counter)

"""f=open('detect_test.log','w')
for item in data_for_export:
	f.write(str(item)+',')"""
