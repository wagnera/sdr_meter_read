from pylab import *
from rtlsdr import *
from scipy import signal
from scipy.signal import butter, lfilter
import math,numpy,time

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    print([low, high])
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



sdr = RtlSdr()

# configure device
fs=2400000
sdr.sample_rate = 2400000
sdr.center_freq = 912200000
#sdr.gain = 4
st=time.time()

# On another machine (typically)
"""client = RtlSdrTcpClient(hostname='127.0.0.1', port=1234)
client.center_freq = 912200000
client.sample_rate = 2400000"""
#data = client.read_samples()

test=[]
while time.time() < st + 120:
	samples = sdr.read_samples(2**16)
	test.extend(samples)
	print("Time remaining: " + str( st + 120 - time.time()))
	"""mag=[]
	for sample in samples:
		mag.append((sample.real**2+sample.imag**2)**0.5)
	mag=numpy.array(mag)
	maxx=numpy.amax(mag)
	test.append(maxx)"""
	#print(maxx)
sdr.close()
test=numpy.array(test)

f=open('sdr_test_data1.log','w')
numpy.save(f,test)
"""for item in test:
	f.write(str(item)+',')"""
#iq_comercial = signal.decimate(samples, 10)
#angle_comercial = np.unwrap(np.angle(iq_comercial))
#demodulated_comercial = np.diff(angle_comercial)
#y = butter_bandpass_filter(demodulated_comercial, 912500155, 912700155, fs*1000, order=6)
plot(test)
show()

