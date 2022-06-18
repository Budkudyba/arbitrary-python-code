# arbitrary-python-code
This is a collection of simple python scripts to show some basic compatency.  
Some of this code is stale and the descriptions my not be accurate.


mfcc2file.py  
Converts all .wav to a MalSpectrum svg image

tracks5.py / track.py  
Uses a raspberry pi with attached camera to automatically identify a circle object (pingpongball). adjust a color threshold for faster real time compute, and then give screen coordinates of the object.

jasper_v1.py  
Samples 5 seconds of sound via microphone input, then uses a speech recogntition to output text

fft.py  
runs and displys a simple fft(fast fourier tranform) on a sound file and produces a plot

autocorrelate.py  
runs a time shifted autocorrelation on seperate files and produces a plot

compare5.py  
attempts to record then identify (within a threshold) an fft correlation between different matching and nonmatching sound files to produce a confidence value to the recorded sound.

test_vid_track7.py  
real time contour filtering and disply of the contours and the area

pwm_4pins.py  
Uses raspberry pi GPIO to create PWM on 4 pins
