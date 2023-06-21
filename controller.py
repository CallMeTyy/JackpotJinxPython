import communication
import constants
import Dataset
import endecoder
import Audio


class Controller:
    # reel 0 is country, 1 is game, 2 is year
    def __init__(self, arduino, serial_com):
        self.reels_stopped = [False, False, False]
        self.reel_values = [-1, -1, -1]
        self.reels_spinning = False
        self.installation_active = False
        self.error_state = False
        self.calibration_done = False
        self.arduino = arduino
        self.comm = serial_com
        self.platform_stage = 0

    def calibration_finished(self):
        self.calibration_done = True
        Audio.play_sfx_loop(0)

    def reel_stopped(self, reel_num, reel_val):
        self.reel_values[reel_num] = reel_val
        self.reels_stopped[reel_num] = True
        self.send(endecoder.encode_reel_stop(reel_num, reel_val))
        print("reels: " + str(self.reel_values))
        if not (False in self.reels_stopped):
            self.reels_spinning = False
            money_lost = Dataset.fetchData((self.reel_values[0], self.reel_values[1], self.reel_values[2]))
            self.start_platform_sequence(money_lost)
            pass

    # this method should be called when a button is pressed, stopping the reel and requesting the data from the reel.
    def stop_button_pressed(self, reel_num):
        if self.reels_spinning:
            self.send(endecoder.encode_reel_requestangle(reel_num))
            self.send(endecoder.encode_button_light_off(reel_num))
            # TODO stop playing reel spinning sound
            # TODO play reel stopped sound
            print("Playing Stop")
            Audio.play_vfx_once(3+reel_num)
            Audio.stop_sfx_loop(reel_num)
            pass

    def lever_pulled(self):
        if not self.installation_active:
            self.installation_active = True
            self.reels_spinning = True
            Audio.stop_sfx_loop(constants.AUDIO_MUSIC)
            for i in range(0, 3):
                self.start_reel_spin(i+1)
            self.send(endecoder.encode_light_pattern(constants.LED_SPIN_PATTERN))
            pass

    def start_reel_spin(self, reel_num):
        # TODO play reel spinning sound
        Audio.play_sfx_loop(reel_num)
        # print(endecoder.encode_reel_setv(reel_num, constants.REEL_SPEED))
        self.send(endecoder.encode_reel_setv(reel_num, constants.REEL_SPEED))
        self.send(endecoder.encode_button_light_on(reel_num))

    def start_platform_sequence(self, money_lost):
        # stage 1: starts immediately
        self.platform_stage_1(money_lost)
        # stage 2: waits until platform is raised (called by platform done decoding)
        # we might not get a signal for this, so we might have to estimate the time)
        # We could also go until winning tune is done
        # stage 3: waits until voice is finished.
        # self.platform_stage_3()
        # stage 4: when platform is fully lowered again
        # self.platform_stage_4()
        # sequence is reset to the start.

    def platform_done(self):
        match self.platform_stage:
            case 1:
                self.platform_stage_2()
            case 3:
                self.platform_stage_4()

    def sound_done(self):
        if self.platform_stage == 2:
            self.platform_stage_3()

    def platform_stage_1(self, money_lost):
        print("reached stage 1")
        self.platform_stage = 1
        # TODO play victory music
        self.send(endecoder.encode_light_pattern(constants.LED_WIN_PATTERN))
        self.send(endecoder.encode_platform_height(money_lost))
        self.send(endecoder.encode_light_height(money_lost))

    def platform_stage_2(self):
        vals = "" + str(self.reel_values[0]) + "," + str(self.reel_values[1]) + "," + str(self.reel_values[2])
        Audio.playVoice((self.reel_values[0], self.reel_values[1], self.reel_values[2]))

    def platform_stage_3(self):
        # TODO shredding sounds start
        Audio.play_vfx_once(constants.AUDIO_SHRED)
        self.send(endecoder.encode_platform_height(0))
        self.send(endecoder.encode_fan_start())

    def platform_stage_4(self):
        self.send(endecoder.encode_fan_stop())
        self.finish_sequence()

    def finish_sequence(self):
        for reel in self.reels_stopped:
            reel = False
        for reel in self.reel_values:
            reel = -1
        self.installation_active = False
        self.send(endecoder.encode_light_pattern(constants.LED_IDLE_PATTERN))
        self.platform_stage = 0

    # if the installation notices a problem in the hardware this method will stop it in its tracks and try to recover
    def external_error(self):
        self.error_state = True

    # this should reset the installation to its starting position and recalibrate the reels.
    def reset_installation(self):
        self.calibration_done = False
        self.send(endecoder.encode_sys_recalibrate())

    # emergency stop should stop all moving parts.
    def emergency_stop(self):
        self.error_state = True
        self.send(endecoder.encode_sys_stop())

    def all_good(self):
        return self.calibration_done and not self.error_state

    def send(self, msg):
        self.comm.send_outgoing(msg, self.arduino)


# # testing stuff
# controller = Controller()
# controller.reel_values = [0, 0, 0]
# controller.platform_stage_2()
