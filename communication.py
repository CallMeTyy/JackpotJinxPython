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
    msg = arduino.readline()[:-2]  # the last bit gets rid of the new-line chars
    if len(msg) > 0:
        if constants.DEBUG:
            data_str = str(msg)[2:-1]
            print(data_str)
            return data_str
    return msg


def send_outgoing(msg):
    arduino.write(str.encode(msg))


def process_data():
    while True:
        msg_in = read_incoming()
        endecoder.decode(msg_in)
        process_loop()


def process_loop():
    pass


# initialisiation
if constants.SIMULATED_SERIAL:
    print("Serial now simulated")
else:
    port = get_port()
    baud_rate = constants.BAUD_RATE
    arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=0)

send_outgoing("hello!")
read_incoming()
process_data()




