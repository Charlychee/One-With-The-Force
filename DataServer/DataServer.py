import socket
from util.CircularList import CircularList
from time import time
from matplotlib import pyplot as plt
from util.logger import Logger

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 55301  # Port to listen on (non-privileged ports are > 1023)

log = Logger(local_path="Logs/serverlog.txt")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Listening for connection")
    s.listen()
    conn, addr = s.accept()
    attention = CircularList([], 60)
    meditation = CircularList([], 60)
    refresh_time = 0.5  # update the plot every 0.1s (10 FPS)
    with conn:
        print(f"Connected to {addr}")
        previous_time = 0
        while True:
            peek_data = conn.recv(1024, socket.MSG_PEEK)
            index = peek_data.find(b'\n')
            if index >= 0:
                index += 1
            else:
                continue
            data = conn.recv(index).decode('utf8')

            log.log_string(data)

            current_time = time()
            if current_time - previous_time > refresh_time:
                previous_time = current_time
                plt.subplot(211)
                plt.cla()
                plt.xlabel('Time')
                plt.ylabel('Level')
                plt.title('Attention')
                plt.plot(attention)
                plt.subplot(212)
                plt.cla()
                plt.xlabel('Time')
                plt.ylabel('Level')
                plt.title('Meditation')
                plt.plot(meditation)
                plt.show(block=False)
                plt.pause(0.001)

            sample_time, value_type, value = data.split(',')

            if value_type == 'attention':
                attention.add(int(value))
            elif value_type == 'meditation':
                meditation.add(int(value))

