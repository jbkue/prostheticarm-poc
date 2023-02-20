from machine import Pin, PWM
from time import sleep


def initSer(pin):
  servo = PWM(Pin(pin))
  servo.freq(50)
  return servo

def collaps():
  	pointer.duty_ns(2000000)
	middle.duty_ns(350000)
	ring.duty_ns(1900000)
	pinky.duty_ns(550000)
	return False

def extend():
 	pointer.duty_ns(400000)
	middle.duty_ns(2000000)
	ring.duty_ns(350000)
	pinky.duty_ns(2000000)
	return True


pointer = initSer(14)
middle = initSer(15)
ring = initSer(16)
pinky = initSer(17)

while True:
	sleep(3)
	extend()
	print("open")
	sleep(3)
	collaps()
	print("closed")
	sleep(3)


#pointer works as intended
#middle finger is opposite
#ring finger works as intended change duty cycle to 1900000 for it to draw less current
#pinky finger is opposite change duty cycle in extended from 350000 to 550000 to draw less current