import os, sys, inspect, thread, time, math
from datetime import datetime
import Leap
import UR3
import Trala_Origem
# import FuzzyMethod
import numpy as np
import Barreira
# import FuzzyMethodHardNew
import NewTryfuzzy
import Data

a = 0


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    fingerStatusCount = np.zeros(5)
    i = 0
    vel = 0
    # menor_euc_ant = 0
    cont2 = 0

    # numero de amostras para ver se ta aproximando ou afastando
    menor_euc = np.zeros(5)
    media = np.zeros(2)
    cont3 = 0

    tam = 300
    datapos = 0
    robot_pos = np.zeros([tam, 3])
    hand_pos = np.zeros([tam, 3])
    robot_vel = np.zeros(tam)
    euclidean = np.zeros(tam)
    stamp = np.zeros(tam)






    def on_init(self, controller):
        print "Initialized"
        controller.set_policy(controller.POLICY_ALLOW_PAUSE_RESUME)
        controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)
        # print controller.is_paused()
        aux = 0
        while aux < 5:
            # Loop to initialize Camera
            time.sleep(0.05)
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
        global a, Euc, cont
        # Get the most recent frame and report some basic information
        if Barreira.barrel() == 1:

            frame = controller.frame()

            Euc = np.zeros(len(frame.hands))
            cont = 0

            if a == 0:
                print "Iniciando robo"
                time.sleep(1)
                UR3.Iniciarobot(1)
                print "Robo Iniciado"
                a += 1


            # amos2=30
            # menor_euc = np.zeros(amos2)

            # Get Gestures
            for hand in frame.hands:
                # if a != 1:
                #     print("Coloque a mao para calibrar (10 s)")
                #     time.sleep(10)
                #     n = 0
                #     while n <= 2000:
                #         X = hand.palm_position[0]
                #         Y = hand.palm_position[1]
                #         Z = hand.palm_position[2]
                #
                #         pos = UR3.readPos_Co()
                #         print("Robot_Pos(x,y,z): ", pos)
                #         print "Palm position:  ", hand.palm_position
                #
                #         Teste3D.calibra(X,Y,Z)
                #         n += 1
                #     print("Calibrado!!!!!!")
                #     a = 1

                Xl = hand.palm_position[0]
                Yl = hand.palm_position[1]
                Zl = hand.palm_position[2]
                [Xml, Yml, Zml] = Trala_Origem.muda_origem(Xl, Yl, Zl)
                [Xr, Yr, Zr] = UR3.readPos_Co()
                Euc[cont] = math.sqrt(((Xml - Xr) ** 2.0) + ((Yml - Yr) ** 2.0) + ((Zml - Zr) ** 2.0))
                # print('Distancia Euclidiana da mao esquerda: ', Euc, ' ID: ', hand.id, ' n maos: ', len(frame.hands))
                cont += 1
                # print ('X: ' + str(Xml) + 'Y: ' + str(Yml) + 'Z: ' + str(Zml))
                # print ('Xr: ' + str(Xr) + 'Y: ' + str(Yr) + 'Z: ' + str(Zr))

            # 112 a 179 dedos
            #         fingerData = np.zeros(5)
            #
            #         if hand.stabilized_palm_position[1] >= 200 and hand.stabilized_palm_position[1] <= 400:
            #
            #             for finger in hand.fingers:
            #
            #                 if finger.is_extended == 1 and finger.type == 0:
            #                     fingerData[0] = 1
            #                 elif finger.is_extended == 0 and finger.type == 0:
            #                     fingerData[0] = 0
            #
            #                 if finger.is_extended == 1 and finger.type == 1:
            #                     fingerData[1] = 1
            #                 elif finger.is_extended == 0 and finger.type == 1:
            #                     fingerData[1] = 0
            #
            #                 if finger.is_extended == 1 and finger.type == 2:
            #                     fingerData[2] = 1
            #                 elif finger.is_extended == 0 and finger.type == 2:
            #                     fingerData[2] = 0
            #
            #                 if finger.is_extended == 1 and finger.type == 3:
            #                     fingerData[3] = 1
            #                 elif finger.is_extended == 0 and finger.type == 3:
            #                     fingerData[3] = 0
            #
            #                 if finger.is_extended == 1 and finger.type == 4:
            #                     fingerData[4] = 1
            #                 elif finger.is_extended == 0 and finger.type == 4:
            #                     fingerData[4] = 0
            #
            #             if fingerData[0] == 1:
            #                 self.fingerStatusCount[0] += 1
            #             if fingerData[1] == 1:
            #                 self.fingerStatusCount[1] += 1
            #             if fingerData[2] == 1:
            #                 self.fingerStatusCount[2] += 1
            #             if fingerData[3] == 1:
            #                 self.fingerStatusCount[3] += 1
            #             if fingerData[4] == 1:
            #                 self.fingerStatusCount[4] += 1
            #
            #     self.i += 1
            #     amos = 30  # number of samples to verify gestures
            #
            #     if self.i == amos:
            #
            #         if np.array_equal(self.fingerStatusCount, [0, amos, 0, 0, 0]):
            #             print("One")
            #         elif np.array_equal(self.fingerStatusCount, [0, amos, amos, 0, 0]):
            #             print("Two")
            #         elif np.array_equal(self.fingerStatusCount, [0, 0, amos, amos, amos]) or np.array_equal(
            #                 self.fingerStatusCount,
            #                 [0, amos, amos, amos,
            #                  0]):
            #             print("Three")
            #         elif np.array_equal(self.fingerStatusCount, [0, amos, amos, amos, amos]):
            #             print("Four")
            #         elif np.array_equal(self.fingerStatusCount, [amos, amos, amos, amos, amos]):
            #             print("Five")
            #         elif self.fingerStatusCount[0] > amos and self.fingerStatusCount[1] > amos and self.fingerStatusCount[
            #             2] > amos and self.fingerStatusCount[3] > amos and self.fingerStatusCount[4] > amos:
            #             print("Conflict of information, More the one hand")
            #         else:
            #             print("Nothing detect, no hands in the area or no command detected")
            #
            #         self.fingerStatusCount = [0, 0, 0, 0, 0]
            #         self.i = 0

            # print('Distancia eucli: ', len(Euc))

            # print(self.cont2)
            if len(Euc) != 0:
                cont = 0
                self.menor_euc[self.cont2] = Euc[cont]
                cont += 1
                while cont != len(Euc):
                    if Euc[cont] < self.menor_euc[self.cont2]:
                        self.menor_euc[self.cont2] = Euc[cont]
                    cont += 1
                self.cont2 += 1
            # print(self.menor_euc)
            # print('Menor distancia euclidiana: ', menor_euc)
            # FuzzyMethod.fuzzy_sugeno(menor_euc, 1000)

            # if self.cont3 == 2:
            #     self.cont3 = 0
            #     if self.menor_euc[(self.cont2-1)] < 400:
            #         v = FuzzyMethodHardNew.Fuzzyhard('centroid', self.media[0], self.media[1], self.vel)
            #         UR3.sendVel(v)
            #         self.vel = v
            #     elif self.menor_euc[(self.cont2-1)] > 400:
            #         UR3.sendVel(1)
            #         self.vel = 1
            if self.cont3 == 2:
                self.cont3 = 0
                if self.menor_euc[(self.cont2 - 1)] < 115:
                    # UR3.sendVel(0) 75
                    UR3.pauseRobot()
                    self.vel = 0
                    self.robot_vel[self.datapos] = 0
                elif 550 > self.menor_euc[(self.cont2 - 1)] >115:
                    UR3.resumeRobot()
                    v = NewTryfuzzy.Fuzzyhard('centroid', self.media[0], self.media[1], self.vel)
                    UR3.sendVel(v)
                    self.vel = v
                    self.robot_vel[self.datapos] = v
                else:
                    UR3.resumeRobot()
                    UR3.sendVel(1)
                    self.vel = 1
                    self.robot_vel[self.datapos] = 1

                self.euclidean[self.datapos] = self.media[1]
                self.robot_pos[self.datapos] = UR3.readPos_Co()
                # print "Robot Position:"
                # print self.robot_pos[self.datapos]
                for hand in frame.hands:
                    Xl = hand.palm_position[0]
                    Yl = hand.palm_position[1]
                    Zl = hand.palm_position[2]
                    [Xml, Yml, Zml] = Trala_Origem.muda_origem(Xl, Yl, Zl)
                    print "Hand Position in Robot's plane"
                    print [Xml, Yml, Zml]
                    self.hand_pos[self.datapos] = [Xml, Yml, Zml]
                self.stamp[self.datapos] = time.time()
                # print("Amostra n: " + str(self.datapos))
                self.datapos += 1

            if self.datapos == len(self.robot_vel):
                self.datapos = 0
                Data.dataFrameCobot(self.stamp, self.robot_pos, self.hand_pos, self.robot_vel, self.euclidean, 'data3',
                                    '1')
                # print('dados enviados')
                # time.sleep(10)
                # print('pegando mais dados')

            if self.cont2 == len(self.menor_euc):
                self.media[self.cont3] = np.mean(self.menor_euc)
                self.cont3 += 1
                self.cont2 = 0


        else:
            UR3.resumeRobot()
            UR3.sendVel(1)
            self.vel = 1


def main():
    # delay to start the experiment
    time.sleep(1)
    # UR3.Iniciarobot(1)


    controller = Leap.Controller()
    # Create a sample listener and controller
    listener = SampleListener()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Inciciando Robo


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        time.sleep(0.2)
        UR3.Iniciarobot(0)
        time.sleep(0.1)
        device = controller.devices[0]
        time.sleep(0.2)
        controller.set_paused(True)
        if device.is_valid:
            print "Range: %f -- HorizontalAngle(X): %f --  VerticalAngle(Z): %f  " % (
                device.range, device.horizontal_view_angle, device.vertical_view_angle)
        else:
            print device.is_valid

        controller.remove_listener(listener)
        time.sleep(0.5)
        UR3.sendVel(1)



if __name__ == "__main__":
    main()
