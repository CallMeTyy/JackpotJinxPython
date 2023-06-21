import io

import communication
import constants
import controller
import endecoder


def process_loop(com, ardui, contr):
    while True:
        msg = com.read_incoming(ardui)
        if len(msg) > 0:
            # if constants.DEBUG:
            #     print(msg)
            endecoder.decode(msg, contr)


comm = communication.Communication()
arduino = comm.initialise(constants.BAUD_RATE)
# arduino_with_io = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
controller = controller.Controller(arduino, comm)
process_loop(comm, arduino, controller)


