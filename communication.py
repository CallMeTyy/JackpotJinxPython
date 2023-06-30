from collections import deque

import serial
import serial.tools.list_ports


import constants
import endecoder


class Communication:


    def __init__(self):
        self.buffer = deque(["DUMMY"])
        self.ledbuffer = deque(["DUMMY"])
        self.port_list = [constants.ARDUINO_PORT_MAC, constants.ARDUINO_PORT_WINDOWS,
                          constants.ARDUINO_PORT_WINDOWS2,constants.ARDUINO_PORT_WINDOWSB,constants.ARDUINO_PORT_RASPI,
                          constants.ARDUINO_PORT_WINDOWSC,constants.ARDUINO_PORT_RASPI3]
        self.led_port_list = [constants.ARDUINO_PORT_RASPI,constants.ARDUINO_PORT_RASPI2,constants.ARDUINO_PORT_RASPI4,constants.ARDUINO_PORT_WINDOWSD]


    def get_port(self):
        """Retrieves all ports from device and returns the port applicable for the device OS"""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            short = str(p).split(' ')[0]
            if constants.COMM_DEBUG:
                print(p)
                print(short)
            if short in self.port_list:
                self.port_list.remove(short)
                return short

    def get_port_led(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            short = str(p).split(' ')[0]
            if constants.COMM_DEBUG:
                print(p)
                print(short)
            if short in self.led_port_list:
                self.led_port_list.remove(short)
                return short

    def read_incoming(self, arduino):
        """Reads all incoming messages and decodes them into strings"""
        msg = arduino.readline()[:]  # the last bit gets rid of the new-line chars
        data_str = str(msg)[2:-1]
        if len(data_str) > 0:
            data_str = data_str[:-4]
            if constants.COMM_DEBUG:
                if data_str != "OK" or constants.COMM_PRINT_OK:
                    print("in:" + data_str)
            return data_str
        return data_str

    def buffer_outgoing(self, msg):
        """Sends the message to the specified arduino"""
        if constants.USE_LED_ARDUINO and msg[:2] == "LE":
            if constants.COMM_DEBUG:
                print("bufL:" + msg)
            if len(self.ledbuffer) == 0:
                self.ledbuffer.append("ND")
            self.ledbuffer.append(msg)
        else:
            if constants.COMM_DEBUG:
                print("buf:" + msg)
            if len(self.buffer) == 0:
                    self.buffer.append("ND")
            self.buffer.append(msg)
        # arduino.write(str.encode(msg + '\n'))

    def send_next_msg(self, arduino):
        if len(self.buffer) > 0:
            old = self.buffer.popleft()
            if constants.COMM_DEBUG:
                print("deleted:" + old)
        self.send_msg(arduino)

    def send_next_msg_ledarduino(self,ledarduino):
        if len(self.ledbuffer) > 0:
            old = self.ledbuffer.popleft()
            if constants.COMM_DEBUG:
                print("deletedL:" + old)
        self.send_msg_led(ledarduino)
    
    def send_msg_led(self, arduino):
        msg = endecoder.encode_nodata()
        if len(self.ledbuffer) > 0:
            msg = self.ledbuffer[0]
        if constants.COMM_DEBUG or constants.DEBUG_LED:
            if constants.COMM_PRINT_OK or msg is not "ND":
                print("outL:" + msg)
        if msg == "ND":
            msg == ""
        if constants.USE_LED_ARDUINO and msg[:3] != "LE2":
            arduino.write(str.encode(msg + '\n'))

    def send_msg(self, arduino):
        msg = endecoder.encode_nodata()
        if len(self.buffer) > 0:
            msg = self.buffer[0]
        if constants.COMM_DEBUG and msg != "ND":
            print("out:" + msg)
        arduino.write(str.encode(msg + '\n'))

    def initialise(self, baudrate, isNormalArduino = True):
        """Retrieves the port and sets up the arduino for communication"""
        port = self.get_port() if isNormalArduino else self.get_port_led()
        
        baud_rate = constants.BAUD_RATE
        arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=1)
        print("Initialised Device on port "+port)
        return arduino





