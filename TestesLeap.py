import os, sys, inspect, thread, time, math
import Leap
import numpy as np




class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    fingerStatusCount = np.zeros(5)
    i = 0

    def on_init(self, controller):
        print "Initialized"
        controller.set_policy(controller.POLICY_ALLOW_PAUSE_RESUME)
        controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)
        # print controller.is_paused()
        aux = 0
        time.sleep(0.1)
        while aux < 5:
            # Loop to initialize Camera
            controller.set_paused(False)
            aux = aux + 1
            print "Try Connect to LeapMotion"

    def on_connect(self, controller):
        print "Connected"
        # Disable "Orientacion automatica de rastreo"
        controller.config.set("tracking_processing_auto_flip", False);
        # Enable the robust mode to improves the tracking and correct IR from environment.
        controller.config.set("robust_mode_enabled", True);
        controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"
        # controller.set_paused(True)

    def on_exit(self, controller):
        print "Exited"
        controller.set_paused(True)

    def on_frame(self, controller):


        frame = controller.frame()

        for hand in frame.hands:
            fingerData = np.zeros(5)

            if hand.stabilized_palm_position[1] >= 200 and hand.stabilized_palm_position[1] <= 400:

                for finger in hand.fingers:

                    if finger.is_extended == 1 and finger.type == 0:
                        fingerData[0] = 1
                    elif finger.is_extended == 0 and finger.type == 0:
                        fingerData[0] = 0

                    if finger.is_extended == 1 and finger.type == 1:
                        fingerData[1] = 1
                    elif finger.is_extended == 0 and finger.type == 1:
                        fingerData[1] = 0

                    if finger.is_extended == 1 and finger.type == 2:
                        fingerData[2] = 1
                    elif finger.is_extended == 0 and finger.type == 2:
                        fingerData[2] = 0

                    if finger.is_extended == 1 and finger.type == 3:
                        fingerData[3] = 1
                    elif finger.is_extended == 0 and finger.type == 3:
                        fingerData[3] = 0

                    if finger.is_extended == 1 and finger.type == 4:
                        fingerData[4] = 1
                    elif finger.is_extended == 0 and finger.type == 4:
                        fingerData[4] = 0

                if fingerData[0] == 1:
                    self.fingerStatusCount[0] += 1
                if fingerData[1] == 1:
                    self.fingerStatusCount[1] += 1
                if fingerData[2] == 1:
                    self.fingerStatusCount[2] += 1
                if fingerData[3] == 1:
                    self.fingerStatusCount[3] += 1
                if fingerData[4] == 1:
                    self.fingerStatusCount[4] += 1

        self.i += 1
        amos = 30  # number of samples

        if self.i == amos:

            if np.array_equal(self.fingerStatusCount, [0, amos, 0, 0, 0]):
                print("One")
            elif np.array_equal(self.fingerStatusCount, [0, amos, amos, 0, 0]):
                print("Two")
            elif np.array_equal(self.fingerStatusCount, [0, 0, amos, amos, amos]) or np.array_equal(self.fingerStatusCount,
                                                                                               [0, amos, amos, amos,
                                                                                                0]):
                print("Three")
            elif np.array_equal(self.fingerStatusCount, [0, amos, amos, amos, amos]):
                print("Four")
            elif np.array_equal(self.fingerStatusCount, [amos, amos, amos, amos, amos]):
                print("Five")
            elif self.fingerStatusCount[0] > amos and self.fingerStatusCount[1] > amos and self.fingerStatusCount[2] > amos and self.fingerStatusCount[3] > amos and self.fingerStatusCount[4] > amos:
                print("Conflict of information, More the one hand")
            else:
                print("Nothing detect, no hands in the area or no command detected")

            self.fingerStatusCount = [0, 0, 0, 0, 0]
            self.i = 0


def main():
    # delay to start the experiment
    time.sleep(1)

    # fingerStatusCount = np.zeros(5)

    controller = Leap.Controller()
    # Create a sample listener and controller
    listener = SampleListener()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        device = controller.devices[0]
        controller.set_paused(True)
        if device.is_valid:
            print "Range: %f -- HorizontalAngle(X): %f --  VerticalAngle(Z): %f  " % (
                device.range, device.horizontal_view_angle, device.vertical_view_angle)
        else:
            print device.is_valid

        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
