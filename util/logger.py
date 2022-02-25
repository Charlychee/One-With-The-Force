from datetime import datetime
import os
import socket


class Logger:
    local = False
    network = False

    def __init__(self, *, local_path: str = None, network_address: str = None, network_port: int = None):
        if local_path:
            split_path = os.path.splitext(local_path)
            self.log = open(split_path[0] + datetime.now().strftime("%Y-%m-%d %H-%m-%S") + split_path[1], 'w')
            self.local = True
        if network_address and network_port:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((network_address, network_port))
                self.network = True
            except:
                print("Couldn't connect to data server")

    def __del__(self):
        if self.network:
            self.sock.close()
        if self.local:
            self.log.close()

    def log_data(self, time, value_type, value):
        log_str = str(time) + "," + value_type + "," + str(value) + "\n"
        if self.local:
            self.log.write(log_str)
            self.log.flush()
        if self.network:
            self.sock.sendall(log_str.encode())

    def log_string(self, string: str):
        if self.local:
            self.log.write(string)
            self.log.flush()

        if self.network:
            self.sock.sendall(string.encode())
