from PyQt5.QtCore import pyqtSignal, QObject
from NeuroSkyPy import NeuroSkyPy
from time import sleep
from util.logger import Logger


class NeuroskyWorker(QObject):
    opacity_signal = pyqtSignal(float)
    finished = pyqtSignal()
    attention = 0
    meditation = 0
    neuropy = None
    log_writer = None

    def run(self):
        self.log_writer = Logger(local_path="Logs/data.csv", network_address="192.168.50.99", network_port=55301)
        print("Logging Started")
        self.neuropy = NeuroSkyPy('COM7')
        self.neuropy.setCallBack("attention", self.attention_callback)
        self.neuropy.setCallBack("meditation", self.meditation_callback)
        self.neuropy.start()
        print("Neuropy Started")
        try:
            while True:
                sleep(0.2)
        finally:
            self.neuropy.stop()

        self.finished.emit()

    def attention_callback(self, attention_value, time_taken):
        """this function will be called everytime NeuroPy has a new value for attention"""
        self.log_writer.log_data(time_taken, "attention", attention_value)
        self.attention = attention_value
        print("Value of attention is: ", attention_value)
        self.send_opacity()

    def meditation_callback(self, meditation_value, time_taken):
        """this function will be called everytime NeuroPy has a new value for attention"""
        self.log_writer.log_data(time_taken, "meditation", meditation_value)
        self.meditation = meditation_value
        print("Value of meditation is: ", meditation_value)
        self.send_opacity()

    def send_opacity(self):
        # TODO: Make proper algorithm for choosing an opacity
        self.opacity_signal.emit(self.attention / 100)

