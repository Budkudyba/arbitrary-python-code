import time
from pylab import*
from scipy.io import wavfile
import numpy as np
import record
import speech_recognition as sr

print("welcome")
name = "test.wav"
record.rec(name,5)


r = sr.Recognizer()
with sr.WavFile('test.wav') as source:
    audio = r.record(source)

try:
    print('detected: ' + r.recognize(audio))
except LookupError:
    print('nothing detected')
          
