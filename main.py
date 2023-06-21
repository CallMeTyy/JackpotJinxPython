import communication
import constants
import controller
import endecoder


def process_loop(arduino, controller):
    while True:
        msg = communication.read_incoming(arduino)
        if len(msg) > 0:
            endecoder.decode(msg, controller)


arduino = communication.initialise(constants.BAUD_RATE)
controller = controller.Controller()
process_loop(arduino, controller)


