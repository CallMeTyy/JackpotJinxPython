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
    print("reading...")
    msg = arduino.readline()[:-2]  # the last bit gets rid of the new-line chars
    if len(msg) > 0:
        if constants.DEBUG:
            data_str = str(msg)[2:-1]
            print(data_str)
            return data_str
    return msg


def send_outgoing(msg):
    # if constants.DEBUG:
    #     print(msg)
    arduino.write(str.encode(msg))


def process_data():
    while True:
        msg_in = read_incoming()
        msg_out = encode_decode(msg_in)
        if len(msg_out) > 0:
            send_outgoing(msg_out)


def encode_decode(msg):
    # return "pong"
    return endecoder.Encode(endecoder.Decode(msg))


#initialisiation
port = get_port()
baud_rate = constants.BAUD_RATE
arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=0)

send_outgoing("hello!")
read_incoming()
process_data()




