import RPi.GPIO as GPIO
import time
print("welcome")

pins = [12,13,15,16]
GPIO.setmode(GPIO.BOARD)
for p in pins:
	GPIO.setup(p, GPIO.OUT)
	print(str(p))
freq = 4000
duty = 100
p = []
for pn in pins:
	p.append(GPIO.PWM(pn, 100))
for pn in p:
	pn.start(duty)
	print(str(pn))
raw_input('Press return to stop:')   # use raw_input for Python 2
for pn in p:
	pn.stop()
GPIO.cleanup()
