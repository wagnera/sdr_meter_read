from pylab import *
from rtlsdr import *
from scipy import signal
from scipy.signal import butter, lfilter
import math,time
import numpy as np 

f=open('/home/anthony/sdr_test_data1.log','r')
samples=np.load(f)
print("Loaded data from file")

#mag=[]
#for sample in samples:
#	mag.append((sample.real**2+sample.imag**2)**0.5)
processed_data=np.absolute(samples)
print("Calculated magnitude")

#processed_data=np.copy(data)
num_decimate=4
data_decimate=0
for i in range(num_decimate):
	if i == data_decimate:
		data=np.copy(processed_data)
	processed_data = signal.decimate(processed_data, 10)
	print("Completed Decimate: "+ str(i+1))
processed_data=(processed_data - processed_data.mean()) / processed_data.std()
std_dev=(np.var(processed_data))**0.5
peaks=np.where( processed_data > 10 )
print(peaks[0][0])

for i in range(len(peaks[0])):
	msg_data_index=peaks[0][i]*10**(num_decimate-data_decimate)
	print(msg_data_index)
	msg_data=data[msg_data_index-30000:msg_data_index+15000]
	#msg_data=data[98500:110500]
	print(len(data))
	"""plt.subplot(2, 1, 1)
	plot(data)
	plt.subplot(2, 1, 2)
	plot(processed_data)"""
	plot(msg_data)
	show()
	f=open('sdr_good_msg'+str(i+10)+'.log','w')
	np.save(f,msg_data)
