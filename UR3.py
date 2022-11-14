import os, sys, inspect, thread, time, math
import win_inet_pton
import socket
from pyModbusTCP.client import ModbusClient

HOST = "10.20.38.10"
ModBus = ModbusClient(host=HOST, port=502, auto_open=True)
PORT_SPEED = 30002
PORT_STOP_PLAY = 29999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT_SPEED))
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((HOST, PORT_STOP_PLAY))


# vel = 1
# aux = 0  # diminui velocidade.... aux=1 aumenta velocidade
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)  # compute negative value
    return val  # return positive value as is


def readPos_Co():
    ReadPoseX = ModBus.read_input_registers(400)  # pose x in base frame
    ReadPoseY = ModBus.read_input_registers(401)  # pose y in base frame
    ReadPoseZ = ModBus.read_input_registers(402)  # pose z in base frame
    ModBus.close()
    if (ReadPoseX is not None):
        X = twos_comp(ReadPoseX[0], 16) / 10.0
    if (ReadPoseY is not None):
        Y = twos_comp(ReadPoseY[0], 16) / 10.0
    if (ReadPoseZ is not None):
        Z = twos_comp(ReadPoseZ[0], 16) / 10.0

    return (X, Y, Z)

def Iniciarobot(boo):
    var = ModBus.read_holding_registers(129, 1)
    # print(var)
    if var == [0] and boo == 1:
        print("Iniciando Movimento")
        ModBus.write_single_register(129, 1)
    elif var == [1] and boo == 0:
        print("Parando Movimento")
        ModBus.write_single_register(129, 0)
    else:
        if boo == 1:
            print("O robo ja esta andando")
        elif boo == 0:
            print("O robo ja esta parado")
        else:
            print("Comando nao reconhecido")
    return

def pauseRobot():
    cmd = "pause" + "\n"
    s2.send(cmd.encode())
    return

def resumeRobot():
    cmd = "play" + "\n"
    s2.send(cmd.encode())
    return

def closePopup():
    cmd = "close popup" + "\n"
    s2.send(cmd.encode())
    return



def Euclidean_distReta(Xm, Ym, Zm, Xr, Yr, Zr):
    Dist_MR = math.sqrt(((Xm - Xr) ** 2.0) + ((Ym - Yr) ** 2.0) + ((Zm - Zr) ** 2.0))
    min = 100.000
    max = 600.000
    a = 1.0 / (max - min)
    b = a * min
    # print ('a: \n', a)
    # print ('b: \n', b)

    if Dist_MR <= min:
        cmd = "set speed" + str(0) + "\n"
        s.send(cmd.encode())

    elif min < Dist_MR <= max:

        vel = a * Dist_MR - b
        # print ('vel: \n', vel)
        cmd = "set speed" + str(vel) + "\n"
        s.send(cmd.encode())
    else:
        cmd = "set speed" + str(1) + "\n"
        s.send(cmd.encode())
    return


def Euclidean_distLog(Xm, Ym, Zm, Xr, Yr, Zr):

    Dist_MR = math.sqrt(((Xm - Xr) ** 2.0) + ((Ym - Yr) ** 2.0) + ((Zm - Zr) ** 2.0))
    min = 200.000
    max = 1000.000
    n = 500
    a = (n - 1.0) / (max - min)
    b = a * min
    # print ('a: \n', a)
    # print ('b: \n', b)

    if Dist_MR <= min:
        cmd = "set speed" + str(0) + "\n"
        s.send(cmd.encode())

    elif min < Dist_MR <= max:

        vel = math.log(a * Dist_MR - b,n)
        # print ('vel: \n', vel)
        cmd = "set speed" + str(vel) + "\n"
        s.send(cmd.encode())
    else:
        cmd = "set speed" + str(1) + "\n"
        s.send(cmd.encode())
    return


def sendVel(vel):
    cmd = "set speed" + str(vel) + "\n"
    s.send(cmd.encode())
    return


def liga():
    cmd = "power on" + "\n"
    s2.send(cmd.encode())
    return

def desliga():
    cmd = "power off" + "\n"
    s2.send(cmd.encode())
    return

def desligaf():
    cmd = "shutdown" + "\n"
    s2.send(cmd.encode())
    return



def comeca():
    cmd = "brake release" + "\n"
    s2.send(cmd.encode())
    return

def ligarBot():
    liga()
    time.sleep(1)
    comeca()
    return

def loadProgram(file):
    cmd = "load " + file + "\n"
    s2.send(cmd.encode())
    return
# def readVel():
#     ReadVelX = ModBus.read_input_registers(410)  # pose x in base frame
#     ReadVelY = ModBus.read_input_registers(411)  # pose y in base frame
#     ReadVelZ = ModBus.read_input_registers(412)  # pose z in base frame
#     ModBus.close()
#     if (ReadVelX is not None):
#         X = twos_comp(ReadVelX[0], 16) / 10.0
#     if (ReadVelY is not None):
#         Y = twos_comp(ReadVelY[0], 16) / 10.0
#     if (ReadVelZ is not None):
#         Z = twos_comp(ReadVelZ[0], 16) / 10.0

    # if (aux == 0):
    #     vel = vel - 0.1
    #     if (vel < 0.1):
    #         aux = 1
    # else:
    #     vel = vel + 0.1
    #     if (vel > 0.9):
    #         aux = 0
    # time.sleep(0.1)
