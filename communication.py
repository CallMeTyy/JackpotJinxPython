import serial
import serial.tools.list_ports

import constants
import endecoder


def get_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
        short = str(p).split(' ')[0]
        print(short)
        if short == constants.ARDUINO_PORT_MAC:
            return short
        elif short == constants.ARDUINO_PORT_WINDOWS:
            return short


def read_incoming():
    msg = arduino.readline()[:]  # the last bit gets rid of the new-line chars
    data_str = str(msg)[2:-1]
    if len(data_str) > 0:
        # data_str = str(msg)[2:-1]
        data_str = data_str[:-4]
        # if constants.DEBUG:
        #     print(data_str)
        return data_str
    return data_str


def send_outgoing(msg):
    arduino.write(str.encode(msg))


def process_data():
    msg = ""
    while True:
        msg_in = read_incoming()
        if len(msg_in) > 0:
            print(msg_in)
            # word_end_pos = msg.find("\r\n")
            # command = msg[:word_end_pos+2]
            # msg = msg[word_end_pos+2:]
            # print(command)
            # print(msg)
            endecoder.decode(msg_in)


def initialise(baudrate):
    port = get_port()
    baud_rate = constants.BAUD_RATE
    arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=0)
    return arduino





