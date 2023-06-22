import io

import communication
import constants
import controller
import endecoder
import Audio


def process_loop(com, ardui, contr):
    while True:
        msg = com.read_incoming(ardui)
        if len(msg) > 0:
            # if constants.DEBUG:
            #     print(msg)
            endecoder.decode(msg, contr)
        Audio.handle_loops()
        waitDone = Audio.wait_for_voice_done()
        if (not waitDone == -1):
            controller.sound_done(waitDone)


comm = communication.Communication()
arduino = comm.initialise(constants.BAUD_RATE)
# arduino_with_io = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
controller = controller.Controller(arduino, comm)
process_loop(comm, arduino, controller)


