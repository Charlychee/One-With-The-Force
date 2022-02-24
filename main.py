from NeuroSkyPy import NeuroSkyPy
from time import sleep

neuropy = NeuroSkyPy('COM3')


def attention_callback(attention_value):
    """this function will be called everytime NeuroPy has a new value for attention"""
    print("Value of attention is: ", attention_value)


neuropy.setCallBack("attention", attention_callback)

print("starting....")

neuropy.start()

print("started....")
try:
    while True:
        sleep(0.2)
finally:
    neuropy.stop()
