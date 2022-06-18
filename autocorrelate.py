from pylab import*
from scipy.io import wavfile
import scipy.interpolate as interp
import numpy as np
#import math
#import collections

print("welcome")

def getFile(name):
    sampFreq,snd = wavfile.read(name)
    print(name + " Loaded")
    shape = snd.shape
    if len(shape) <= 1:
        chan = snd[:,]
    elif shape[1] >= 1:
        print("taking only 1st channel of " + name)
        chan = snd[:,0] #take only one channel
    else:
        print("something bad happened in finding what channel to take")
    chan = chan/(2.**15)
    dur = float(shape[0])/float(sampFreq)
    print(str(dur)+" seconds at "+ str(sampFreq)+"Hz")
    print(str(shape[0])+" Samples")
    return sampFreq,chan

def chop(rate,snd,length=1,offset=0):
    #define number of samples to use
    #length(s) plus the next power of 2
    print(str(length)+" sample seconds")
    print(str(offset)+" sample offset")
    samp = int(rate*length)
    offset = int(rate*offset)
    top = 1<<(samp-1).bit_length()#find next power of two
    snd = snd[0+offset:top+offset]
    return samp,snd

def getfft(snd,n):     
    p = np.fft.fft(snd,n) #take the fast fourier transform
    nUniqPts = ceil((n+1)/2.0)
    #print(str(nUniqPts)+" nUniqPts")
    p = p[0:nUniqPts]
    p = abs(p)
    p = p/float(n)
    p = p**2

    if n%2>0:#odd number of points fft
        p[1:len(p)] = p[1:len(p)]*2
        #print("fft is odd")
    else:#even
        p[1:len(p)-1] = p[1:len(p)-1]*2
        #print("fft is even")

    #p = 10.0*log10(p)
    return p

def plotfft(p,r):#array and rate
    freqArray = arange(0,float(p.shape[0]),1.0) *(r/p.shape[0])
    plot(freqArray,10*log10(p),color='k')
    xlabel('Frequency (kHz)')
    ylabel('Power (dB)')

files = ['swarm.wav','swarm2.wav','swarm3.wav','swarm4.wav','440_sine.wav',
         'Voice_003.wav']
power = []
blockSize = 1024

for f in files:
    r,s = getFile(f)
    n = len(s)
    #512 fft blocks in 1024 sample size
    blocks = n/blockSize
    print(str(blocks)+" blocks present")
    block = np.zeros((blockSize/2)+1)
    for a in range(blockSize,(n/blockSize*blockSize)-blockSize,blockSize):
        p = getfft(s[a:a+blockSize],blockSize)
        block += p+block    
    avg = block/blocks
    
    subplot(len(files),1,files.index(f))
    plotfft(avg,r)
    title(f)           
    power.append(avg)
show()
"""
    #v = s.var()
    #s = s-s.mean()
    
    #result = r/(v*(np.arange(n,0,-1)))

for x in range(len(power)-1):
    print(files[0]+" with "+ files[x+1])
    cor = correlate(power[0],power[x+1])
    peak = max(cor)
    print(str(peak)+" max")
    index = [i for i, j in enumerate(cor) if j==peak] #find index of max
    offset = index[0] - cor.shape[0]/2
    print(str(offset))
"""






















