import serial
import serial.tools.list_ports
import constants


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
    data = arduino.readline()[:-2]  # the last bit gets rid of the new-line chars
    if constants.DEBUG:
        print(data)
    return data


def send_outgoing(msg):
    pass


def process_data():
    while True:
        msg_in = read_incoming()
        # send the data out to encoding and eventually get a message back to send out
        msg_out = "test message"
        if len(msg_out) > 0:
            send_outgoing(msg_out)



#initialisiation
port = get_port()
baud_rate = constants.BAUD_RATE
arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=0)
box_placable = False
process_data()

