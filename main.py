import io

import communication
import constants
import controller
import endecoder
import Audio


def process_loop(com, ardui, contr):
    """The main loop of the program, controls everything"""
    while True:
        msg = com.read_incoming(arduino)
        if len(msg) > 0:
            endecoder.decode(msg, contr)
        Audio.handle_loops()
        waitDone = Audio.wait_for_voice_done()
        if (not waitDone == -1):
            controller.sound_done(waitDone)


# Initialise the program and start the loop
comm = communication.Communication()
arduino = comm.initialise(constants.BAUD_RATE)
# arduino_with_io = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
controller = controller.Controller(arduino, comm)
process_loop(comm, arduino, controller)


