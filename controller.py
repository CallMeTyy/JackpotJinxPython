import communication
import constants
import Dataset
import endecoder
import Audio


class Controller:
    # reel 0 is country, 1 is game, 2 is year
    def __init__(self, arduino, serial_com, secondarduino = ""):
        """Initialize arduino."""
        self.reels_stopped = [False, False, False]
        self.reel_values = [-1, -1, -1]
        self.reels_spinning = False
        self.stage_1_done = False # [platform_done, sound_done]
        self.installation_active = False
        self.error_state = False
        self.calibration_done = False
        self.arduino = arduino
        self.comm = serial_com
        self.platform_stage = 0
        self.play_shredsound = True
        self.currentMoneyLost = 0
        self.ledarduino = secondarduino

    def calibration_finished(self):
        """Call when calibration is done, start playing the standard music."""
        self.calibration_done = True
        Audio.play_sfx_loop(0)

    def reel_stopped(self, reel_num, reel_val):
        """Set a reel to stopped, if all reels are stopped retrieve datapoint, play according sounds and start next sequence."""
        self.reel_values[reel_num] = reel_val
        self.reels_stopped[reel_num] = True
        self.send(endecoder.encode_reel_stop(reel_num, reel_val))
        if constants.COMM_DEBUG:
            print("reels: " + str(self.reel_values))
        if not (False in self.reels_stopped):
            self.reels_spinning = False
            money_lost = Dataset.fetch_data((self.reel_values[0], self.reel_values[1], self.reel_values[2]))
            if constants.COMM_DEBUG:
                print("money lost: " + str(money_lost))
            self.play_shredsound = money_lost != 0.0
            self.currentMoneyLost = money_lost
            self.start_platform_sequence(money_lost)
            pass

    def stop_button_pressed(self, reel_num):
        """this method should be called when a button is pressed, stopping the reel and requesting the data from the reel."""
        if self.reels_spinning:
            self.send(endecoder.encode_reel_requestangle(reel_num))
            self.send(endecoder.encode_button_light_off(reel_num))
            if constants.AUDIO_DEBUG:
                print("Playing Stop")
            Audio.play_vfx_once(4+reel_num)
            # Audio.stop_sfx_loop(reel_num)
            Audio.stop_sfx_loop(reel_num+1)
            pass

    def lever_pulled(self):
        """Call when lever gets pulled, stops the regular music and starts spinning the reels."""
        if not self.installation_active:
            self.installation_active = True
            self.reels_spinning = True
            Audio.stop_sfx_loop(constants.AUDIO_MUSIC)
            Audio.stop_sfx_loop(0)
            for i in range(0, 3):
                self.start_reel_spin(i)
            self.send(endecoder.encode_light_pattern(constants.LED_SPIN_PATTERN))
            pass

    def start_reel_spin(self, reel_num):
        """Start spinning the specified reel."""
        # print("Reel " + str(reel_num) + " spinning!")
        Audio.play_sfx_loop(reel_num+1)
        # print(endecoder.encode_reel_setv(reel_num, constants.REEL_SPEED))
        self.send(endecoder.encode_reel_setv(reel_num, constants.REEL_SPEED))
        self.send(endecoder.encode_button_light_on(reel_num))

    def start_platform_sequence(self, money_lost):
        """Start platform sequence based on money lost."""
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
        """Call when platform is done rising or lowering."""
        if constants.AUDIO_DEBUG:
            print("platform done!")
        match self.platform_stage:
            case 1:
                self.stage_1_done = True
                self.platform_stage_2()
            case 3:
                self.platform_stage_4()

    def sound_done(self, sound_id):
        match sound_id:
            case 0:     # voice
                if constants.AUDIO_DEBUG:
                    print("voice done!")
                self.platform_stage_3()
            # case 1:     # victory sound
            #     if constants.AUDIO_DEBUG:
            #         print("win sound done!")

    def platform_stage_1(self, money_lost):
        """Play winning music and start raising the platform and lights to the correct values."""
        if self.platform_stage == 0:
            if constants.COMM_DEBUG:
                print("reached stage 1")
            self.platform_stage = 1
            # Audio.play_vfx_once(8)
            Audio.play_sfx_loop(9)
            self.send(endecoder.encode_light_pattern(constants.LED_WIN_PATTERN))
            self.send(endecoder.encode_platform_height(money_lost))
            self.send(endecoder.encode_light_height(money_lost))

    def platform_stage_2(self):
        """Platform has reached the correct height, stop the winning music and start playing the voiceline."""
        if self.platform_stage == 1:
            if self.stage_1_done:
                self.platform_stage = 2
                if constants.COMM_DEBUG:
                    print("reached stage 2")
                self.stage_1_done = False
                vals = "" + str(self.reel_values[0]) + "," + str(self.reel_values[1]) + "," + str(self.reel_values[2])
                Audio.stop_sfx_loop(9)
                # Audio.play_vfx_once(10)
                Audio.playVoice((self.reel_values[0], self.reel_values[1], self.reel_values[2]))

    def platform_stage_3(self):
        """Start 'shredding' the money."""
        if self.platform_stage == 2:
            self.platform_stage = 3
            if constants.COMM_DEBUG:
                print("reached stage 3")
            if self.play_shredsound:
                Audio.play_shredder(self.currentMoneyLost)
            self.send(endecoder.encode_platform_height(0))
            self.send(endecoder.encode_fan_start())

    def platform_stage_4(self):
        """Stop the fans, interaction is now finished."""
        if self.platform_stage == 3:
            self.platform_stage = 4
            if constants.COMM_DEBUG:
                print("reached stage 4")
            self.send(endecoder.encode_fan_stop())
            self.finish_sequence()

    def finish_sequence(self):
        """Call when all interactions are done and prepare for next use."""
        for i in range(0, 3):
            self.reels_stopped[i] = False
            self.reel_values[i] = -1
        self.installation_active = False
        self.send(endecoder.encode_light_pattern(constants.LED_IDLE_PATTERN))
        self.platform_stage = 0
        Audio.play_sfx_loop(0)
        if constants.COMM_DEBUG:
            print("ready for next use!")

    def external_error(self):
        """f the installation notices a problem in the hardware this method will stop it in its tracks and try to recover."""
        self.error_state = True

    def reset_installation(self):
        """This should reset the installation to its starting position and recalibrate the reels."""
        self.calibration_done = False
        self.send(endecoder.encode_sys_recalibrate())

    
    def emergency_stop(self):
        """Emergency stop should stop all moving parts."""
        self.error_state = True
        self.send(endecoder.encode_sys_stop())

    def all_good(self):
        """call when calibrations are successful"""
        return self.calibration_done and not self.error_state

    def send(self, msg):
        """send message to arduino."""
        self.comm.buffer_outgoing(msg)

    def send_next_message(self):
        self.comm.send_next_msg(self.arduino)

    def send_next_message_led(self):
        self.comm.send_next_msg_ledarduino(self.ledarduino)

    def resend_message(self, fromLed = False):
        if fromLed:
            self.comm.send_msg_led(self.ledarduino)
        else:
            self.comm.send_msg(self.arduino)


# # testing stuff
# controller = Controller()
# controller.reel_values = [0, 0, 0]
# controller.platform_stage_2()
