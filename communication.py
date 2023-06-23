import serial
import serial.tools.list_ports

import constants
import endecoder
from collections import deque
import time


class Communication:

    def get_port(self):
        """Retrieves all ports from device and returns the port applicable for the device OS"""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            short = str(p).split(' ')[0]
            if constants.COMM_DEBUG:
                print(p)
                print(short)
            if short == constants.ARDUINO_PORT_MAC:
                return short
            elif short == constants.ARDUINO_PORT_WINDOWS or short == constants.ARDUINO_PORT_WINDOWS2:
                return short
            elif short == constants.ARDUINO_PORT_RASPI:
                return short


    def read_incoming(self, arduino):
        """Reads all incoming messages and decodes them into strings"""
        msg = arduino.readline()[:]  # the last bit gets rid of the new-line chars
        data_str = str(msg)[2:-1]
        if len(data_str) > 0:
            data_str = data_str[:-4]
            if constants.COMM_DEBUG:
                print("in:" + data_str)
            return data_str
        return data_str

    def send_outgoing(self, msg, arduino):
        """Sends the message to the specified arduino"""
        if constants.COMM_DEBUG:
            print("out:" + msg)
        arduino.write(str.encode(msg + '\n'))

    def initialise(self, baudrate):
        """Retrieves the port and sets up the arduino for communication"""
        port = self.get_port()
        baud_rate = constants.BAUD_RATE
        arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=1)
        return arduino





