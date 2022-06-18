import time
from pylab import*
from scipy.io import wavfile
import numpy as np
import record
#import math
#import collections

print("welcome")

log = open("log",'w')

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
    print(str(nUniqPts)+" nUniqPts")
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

    p = 10.0*log10(p)
    return p

def plotfft(p,r):
    freqArray = arange(0,float(p.shape[0]),1.0) *(r/len(p))
    plot(freqArray/1000.0,p,color='k')
    xlabel('Frequency (kHz)')
    ylabel('Power (dB)')

def findMatch(power,threshold):
    peak = []
    offset = []
    match = []
    for x in range(len(power)-1):
        print(files[-1]+" with "+ files[x])
        cor = correlate(power[-1],power[x])
        peak.append(max(cor))
        print(str(peak[-1])+" max")
        index = [i for i, j in enumerate(cor) if j==peak[-1]] #find index of max
        offset.append(index[0] - cor.shape[0]/2)
        print(str(offset[-1]))
        found = False
        if peak[-1]*10 >= thresh:
            if abs(offset[-1]) < 0.001:
                found = True
        print(str(found))
        match.append(found)
    return match,peak,offset

TOTALMATCHES = 0 #total number of matches since running
lastHit = False #indicates a series of matches
consecutive = 0 #TOTALMATCHES in a row
cThresh = 5 #number of consecutive matches to warrent a call
files = ['Voice_003.wav','swarm.wav','swarm2.wav',
         'swarm3.wav','swarm4.wav','440_sine.wav']
valid = [False,True,True,True,True,False]#if cor should proc
loops = 0
while(loops <= 50):
    loops += 1
    
    name = "out"+str(TOTALMATCHES)+".wav"
    record.rec(name,1)
    files.append(name)

    power = []

    for f in files:
        r,s = getFile(f)
        r,s = chop(r,s,.25)
        p = getfft(s,5000)
        subplot(len(files),1,files.index(f))
        plotfft(p,r)
        title(f)
        power.append(s)
    #show()

    thresh = 2.0 #match threshold b/w 1 and 10?

    match,peak,offset = findMatch(power,thresh)
    files.remove(name)
    
    confidence = 0
    hit = False #True if found
    miss= False #True if missmatch
    hitmatch = []
    for v in range(len(valid)):
        if valid[v] == False:
            if match[v] == True:
                miss = True
            if match[v] == False:
                confidence += 1/float(len(match))*100
        if valid[v] == True:
            if match[v] == True:
                confidence += 1/float(len(match))*100
                hitmatch.append(files[v])
                hit = True
    if hit:
        if not miss:
            print("Swarm Maybe found")
            log.write("Trigger "+str(loops)+"\n")
            log.write(time.strftime("%a, %b %d %Y %H:%M:%S\n",time.localtime()))
            print("confidence: "+str(confidence)+"%")
            log.write("matching: "+str(hitmatch))
            del hitmatch[:] #remove hitmatches for next loop
            log.write(" confidence: "+str(confidence)+"%\n")
            TOTALMATCHES += 1
            if lastHit:
                consecutive += 1
                log.write("Consec Match! "+str(consecutive)+"\n")
                if consecutive >= cThresh-1:
                    consecutive = 0
                    lastHit = False
                    print("SWARM FOUND!")
                    log.write("SWARM FOUND!\n")
            else:
                consecutive = 0
            lastHit = True
        else:
            lastHit = False
    else:
        lastHit = False
