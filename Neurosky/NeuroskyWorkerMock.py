from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from time import sleep, time
from util.logger import Logger
import random


class NeuroskyWorkerMock(QObject):
    attention_signal = pyqtSignal(int)
    meditation_signal = pyqtSignal(int)

    finished = pyqtSignal()
    attention = 0
    meditation = 0
    neuropy = None
    log_writer = None

    def run(self):
        print("Start run")
        self.log_writer = Logger(local_path="Logs/data.csv", network_address="192.168.50.99", network_port=55301)
        print("Logging Started")
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.generate_data)
        self.data_timer.start(1000)

    def attention_callback(self, attention_value, time_taken):
        """this function will be called everytime NeuroPy has a new value for attention"""
        self.log_writer.log_data(time_taken, "attention", attention_value)
        self.attention = attention_value
        # print("Value of attention is: ", attention_value)
        self.attention_signal.emit(attention_value)

    def meditation_callback(self, meditation_value, time_taken):
        """this function will be called everytime NeuroPy has a new value for attention"""
        self.log_writer.log_data(time_taken, "meditation", meditation_value)
        self.meditation = meditation_value
        # print("Value of meditation is: ", meditation_value)
        self.meditation_signal.emit(meditation_value)

    def generate_data(self):
        self.attention_callback(random.randint(0, 100), time())
        self.meditation_callback(random.randint(0, 100), time())
        # self.attention_callback(100, time())
        # self.meditation_callback(100, time())
