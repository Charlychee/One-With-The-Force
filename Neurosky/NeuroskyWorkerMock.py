from PyQt5.QtCore import pyqtSignal, QObject
from time import sleep, time
from util.logger import Logger
import random


class NeuroskyWorkerMock(QObject):
    opacity_signal = pyqtSignal(float)
    finished = pyqtSignal()
    attention = 0
    meditation = 0
    neuropy = None
    log_writer = None

    def run(self):
        print("Start run")
        self.log_writer = Logger(local_path="Logs/data.csv", network_address="192.168.50.99", network_port=55301)
        print("Logging Started")
        while True:
            print("Make data")
            self.attention_callback(random.randint(0, 100), time())
            self.meditation_callback(random.randint(0, 100), time())
            sleep(1)

        self.finished.emit()

    def attention_callback(self, attention_value, time_taken):
        """this function will be called everytime NeuroPy has a new value for attention"""
        self.log_writer.log_data(time_taken, "attention", attention_value)
        self.attention = attention_value
        print("Value of attention is: ", attention_value)
        self.send_opacity()
        print("Attention")

    def meditation_callback(self, meditation_value, time_taken):
        """this function will be called everytime NeuroPy has a new value for attention"""
        self.log_writer.log_data(time_taken, "meditation", meditation_value)
        self.meditation = meditation_value
        print("Value of meditation is: ", meditation_value)
        self.send_opacity()
        print("meditation")

    def send_opacity(self):
        # TODO: Make proper algorithm for choosing an opacity
        self.opacity_signal.emit(self.attention / 100)
        print("Send Opacity")
