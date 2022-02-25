from Neurosky.NeuroSkyPy import NeuroSkyPy
from time import sleep
import time

neuropy = NeuroSkyPy('COM7')

log = open("datalog.log", 'w')

def attention_callback(attention_value):
    """this function will be called everytime NeuroPy has a new value for attention"""
    log.write(str(time.time()) + ",attention," + str(attention_value) + "\n")
    log.flush()
    print("Value of attention is: ", attention_value)


def meditation_callback(meditation_value):
    """this function will be called everytime NeuroPy has a new value for attention"""
    log.write(str(time.time()) + ",meditation," + str(meditation_value) + "\n")
    log.flush()
    print("Value of meditation is: ", meditation_value)


neuropy.setCallBack("attention", attention_callback)
neuropy.setCallBack("meditation", meditation_callback)

print("starting....")

neuropy.start()

print("started....")
try:
    while True:
        sleep(0.2)
finally:
    neuropy.stop()
    log.close()
