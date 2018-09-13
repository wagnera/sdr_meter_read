from pylab import *
from rtlsdr import *
from scipy import signal
from scipy.signal import butter, lfilter
import math,time
import numpy as np 

#f=open('sdr_good_msg12.log','r')
#samples=np.load(f)
#print("Loaded data from file")
def process_packet(samples):
	##Signal Detection
	floor=samples[0:500].mean()
	std_dev=samples[0:500].std()
	trigger=floor+10*std_dev
	#trigger=0.5
	edges=signal.convolve(samples, [-1,-1,-1,-1,-1,0,1,1,1,1,1], mode='full', method='auto')
	temp = np.where(samples>trigger)
	start=argmin(edges)
	end=argmax(edges)
	data=samples[start:end]
	len_data=len(data)

	window = signal.boxcar(20)
	processed_data=signal.convolve(data, window, mode='valid', method='auto')
	data_for_mean=processed_data[int(0.25*len_data):int(0.75*len_data)]
	processed_data=(processed_data - data_for_mean.mean()) / data_for_mean.std()
	bit_data=np.sign(processed_data)
	np.place(bit_data, bit_data==-1, [0])
	edges=signal.convolve(bit_data, [-1,0,1], mode='full', method='auto')
	rising_edges=np.where(edges == -1)[0]
	falling_edges=np.where(edges == 1)[0]
	zero_bits=falling_edges[::2]-rising_edges[::2]
	one_bits=-(rising_edges[::2]-falling_edges[::2])
	bit_length=zero_bits[0:20].mean() #get length of a bit in terms of # of samples
	zero_bits=np.rint(zero_bits/bit_length).astype(int)
	one_bits=np.rint(one_bits/bit_length).astype(int)
	packet=[]
	for zero,one in zip(zero_bits,one_bits):
		packet.extend(['1'] * one)
		packet.extend(['0'] * zero)
	print(''.join(packet))

	##plotting
	plt.subplot(2, 1, 1)
	plot(data)
	plt.subplot(2, 1, 2)
	plot(processed_data)
	plot(bit_data,'r')
	plot(edges,'k')
	savefig('testplot_+'+str(time.time())+'.png')
	clf()
	#plot(range(len(bit_data)), y, 'bo')
	#show()

if __name__ == "__main__":
	f=open('sdr_good_msg12.log','r')
	samples=np.load(f)
	print("Loaded data from file")
	process_packet(samples)