import communication
import constants
import controller
import endecoder


def process_loop(ardui, contr):
    while True:
        msg = communication.read_incoming(ardui)
        if len(msg) > 0:
            if constants.DEBUG:
                print(msg)
            endecoder.decode(msg, contr)


arduino = communication.initialise(constants.BAUD_RATE)
controller = controller.Controller()
process_loop(arduino, controller)


