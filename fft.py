
from pylab import*
from scipy.io import wavfile
#from scipy.interpolate import interp1d

print("welcome")
sampFreq, snd1 = wavfile.read('swarm.wav')
snd = snd1[:,0]#take only one channel
print("sound loaded")
print(str(snd.dtype) + " bit wav")
snd = snd/(2.**15)
shape = snd.shape
print(str(shape))
dur = shape[0]/sampFreq
print(str(dur)+" seconds")

timeArray = arange(0,float(shape[0]),1.0)
timeArray = timeArray/sampFreq
timeArray = timeArray * 1000 #ms scale

plot(timeArray,snd,color='k')
ylabel('Amplitude')
xlabel('Time (ms)')
#show()

print("preforming fft of sound file")
n = len(snd)
p = fft(snd) #take the fast fourier transform
nUniqPts = ceil((n+1)/2.0)
print(str(nUniqPts)+" nUniqPts")
p = p[0:nUniqPts]
p = abs(p)

p = p/float(n)
p = p**2

if n%2>0:#odd number of points fft
    p[1:len(p)] = p[1:len(p)]*2
    print("fft is odd")
else:#even
    p[1:len(p)-1] = p[1:len(p)-1]*2
    print("fft is even")
freqArray = arange(0,float(nUniqPts),1.0) *(sampFreq/n)

#p = interp1d(freqArray,p,kind='cubic')

#remove zeros to prevent div0 errors
numz = 0
for i in p:
    if i == 0:
        p[i] = 10**-10
        numz+=1
print(str(numz)+" number of zeroes in data")

#plot(10.0*log10(freqArray/1000.0),10.0*log10(p),color='k')
plot(freqArray/1000.0,10.0*log10(p),color='k')
#plot(freqArray/1000.0,p,color='k')
xlabel('Frequency (kHz)')
ylabel('Power (dB)')
show()

rms = sqrt(mean(snd**2))
print(str(rms))
rms2 = sqrt(sum(p))
print(str(rms2))
