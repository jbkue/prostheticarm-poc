from machine import UART, Pin, PWM, ADC
from time import sleep
import _thread


def initSer(pin):
  servo = PWM(Pin(pin))
  servo.freq(50)
  return servo

def extend():
	pinky.duty_ns(350000)
	ring.duty_ns(350000)
	thumb.duty_ns(1500000)
	return False

def collaps():
	thumb.duty_ns(1500000)
	sleep(1)
	pinky.duty_ns(2000000)
	ring.duty_ns(1900000)
	return True


def currentSensor(pin):
    AREF = 3.3  # internal voltage of RP2xxx
    DEFAULT_OUTPUT_VOLTAGE = 5 / 2  # for when current is 0 on a unipolar psu is Vcc/2
    MILLIVOLT_PER_AMPERE = 185  # mV/A output sensitivity for this particular sensro
    ERROR = 0.26  # for Error, tune as needed
    analogInputPin = ADC(pin)  # Def ADC pin
    currentList = []  # create a list for finding an average of 150 samples
    for i in range(0, 150):
        analogValue = ADC.read_u16(analogInputPin)
        sensor_voltage = ((analogValue / 65535) * AREF)
        sensor_voltage = (sensor_voltage - DEFAULT_OUTPUT_VOLTAGE) * 1000
        dc_current = (sensor_voltage / MILLIVOLT_PER_AMPERE) - ERROR
        currentList.append(dc_current)
    currentAvg = abs(sum(currentList) / len(currentList))
    return currentAvg

pinky = initSer(15)
ring = initSer(14)
thumb = initSer(16)

def ringCollaps():
    for nsec in range(ring.duty_ns(), 2000000, 20000):
        ringSen = round(currentSensor(27), 3)
        if ringSen > .8:
            ring.duty_ns((nsec - 1000))
            print("object grabbed")
        else:
            ring.duty_ns(nsec)
            print(ring.duty_ns())
            print(ringSen)
    return True


def pinkyCollaps():
    for nsec in range(pinky.duty_ns(), 2000000, 20000):
        pinkySen = round(currentSensor(26), 3)
        if pinkySen > .8:
            pinky.duty_ns((nsec - 1000))
            print("object grabbed")
        else:
            pinky.duty_ns(nsec)
            print(pinky.duty_ns())
            print(pinkySen)
    return True


def thumbCollaps():
    for nsec in range(thumb.duty_ns(), 400000, -20000):
        thumbSen = round(currentSensor(28), 3)
        if thumbSen > .6:
            thumb.duty_ns((nsec - 1000))
            print("object grabbed")
        else:
            thumb.duty_ns(nsec)
            print(thumb.duty_ns())
            print(thumbSen)
    return True

handState = False
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=100)
while True:
    emg = str(uart1.read(1))
    if '1' in emg:
        print(emg)
        if handState == False:
            _thread.start_new_thread(pinkyCollaps, ())
            ringCollaps()
            thumbCollaps()
            handState = True
    elif '0' in emg:
        print(emg)
        extend()
        handState = False