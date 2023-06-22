import serial
import serial.tools.list_ports

import constants
import endecoder
from collections import deque
import time

class Communication:
    def __init__(self):
        self.send_buffer = deque()
        self.delay = 0

    def get_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            short = str(p).split(' ')[0]
            if constants.COMM_DEBUG:
                print(p)
                print(short)
            if short == constants.ARDUINO_PORT_MAC:
                return short
            elif short == constants.ARDUINO_PORT_WINDOWS:
                return short


    def read_incoming(self, arduino):
        msg = arduino.readline()[:]  # the last bit gets rid of the new-line chars
        data_str = str(msg)[2:-1]
        if len(data_str) > 0:
            # data_str = str(msg)[2:-1]
            data_str = data_str[:-4]
            if constants.COMM_DEBUG:
                print("in:" + data_str)
            return data_str
        return data_str

    def send_outgoing(self, msg, arduino):
        if constants.COMM_DEBUG:
            print("out:" + msg)
        arduino.write(str.encode(msg + '\n'))


    def initialise(self, baudrate):
        port = self.get_port()
        baud_rate = constants.BAUD_RATE
        arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=1)
        return arduino





