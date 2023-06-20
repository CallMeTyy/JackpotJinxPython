import constants
import Dataset


class Controller:
    # reel 0 is country, 1 is game, 2 is year
    def __init__(self):
        self.reels_stopped = [False, False, False]
        self.reel_values = [-1, -1, -1]
        self.reels_spinning = False
        self.installation_active = False
        self.error_state = False
        self.calibration_done = False

    def calibration_finished(self):
        self.calibration_done = True

    def reel_stopped(self, reel_num, reel_val):
        self.reel_values[reel_num] = reel_val
        self.reels_stopped[reel_num] = True
        if not (False in self.reels_stopped):
            self.reels_spinning = False
            money_lost = Dataset.FetchData((self.reel_values[0], self.reel_values[1], self.reel_values[2]))
            self.platform_sequence(money_lost)
            pass

    def stop_button_pressed(self, reel_num):
        if self.reels_spinning:
            # set reel speed to 0
            # request reel value
            # stop playing reel spinning sound
            # play reel stopped sound
            pass

    def lever_pulled(self):
        if not self.installation_active:
            self.installation_active = True
            self.reels_spinning = True
            # stop playing idle music
            for i in range(0, 2):
                self.start_reel_spin(i)
            # start playing reel spinning music
            pass

    def start_reel_spin(self, reel_num):
        # play reel spinning sound
        # start spinning reel at certain speed defined in constants
        # set LED pattern to spinning
        pass

    def platform_sequence(self, money_lost):
        # stage 1: starts immediately
        self.platform_stage_1(money_lost)
        # stage 2: waits until platform is raised (we might not get a signal for this, so we might have to estimate the time)
        self.platform_stage_2()
        # stage 3: waits until voice is finished.
        self.platform_stage_3()
        # stage 4: when platform is fully lowered again
        self.platform_stage_4()
        # sequence is reset to the start.
        pass

    def platform_stage_1(self, money_lost):
        # TODO play victory music
        # TODO set LED pattern to win
        # TODO start raising platform
        pass

    def platform_stage_2(self):
        # TODO LED bar is set to the right height
        vals = "" + str(self.reel_values[0]) + "," + str(self.reel_values[1]) + "," + str(self.reel_values[2])
        Dataset.PlayVoice(vals)
        # Dataset.PlayVoice((self.reel_values[0], self.reel_values[1], self.reel_values[2]))
        pass

    def platform_stage_3(self):
        # TODO shredding sounds start
        # TODO platform starts lowering again
        # TODO fan turns on
        pass

    def platform_stage_4(self):
        # TODO fans are stopped
        self.finish_sequence()

    def finish_sequence(self):
        for reel in self.reels_stopped:
            reel = False
        for reel in self.reel_values:
            reel = -1
        self.installation_active = False
        pass

    # if the installation notices a problem in the hardware this method will stop it in its tracks and try to recover
    def external_error(self):
        self.error_state = True
        pass

    # this should reset the installation to its starting position and recalibrate the reels.
    def reset_installation(self):
        self.calibration_done = False
        pass

    # emergency stop should stop all moving parts.
    def emergency_stop(self):
        self.error_state = True
        # TODO stop platform engine
        # TODO stop fan
        # TODO stop reels
        pass

    def all_good(self):
        return self.calibration_done and not self.error_state


# testing stuff
controller = Controller()
controller.reel_values = [0, 0, 0]
controller.platform_stage_2()
