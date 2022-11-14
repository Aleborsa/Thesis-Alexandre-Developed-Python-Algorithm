import numpy as np
import math, time
import UR3

# Esse programa tem o intuito de transladar e rotacionar a origem do sensor para coincidir com a do robo UR3


# b = 0
# [dx, dy, dz] = [0, 0, 0]

# A funcao abaixo remete a propiedade de translacao
def translacao(dx, dy, dz, P=[], *args):
    Pl = np.dot(np.matrix([[1, 0, 0, dx],
                           [0, 1, 0, dy],
                           [0, 0, 1, dz],
                           [0, 0, 0, 1]]), P)
    return Pl

# As funcoes abaixo remetem as propiedade de rotacao em torno dos eixos X, Y, Z
def rotacaoX(theta, P=[], *args):
    Pl = np.dot(np.matrix([[1, 0, 0, 0],
                           [0, math.cos(theta), (-1) * math.sin(theta), 0],
                           [0, math.sin(theta), math.cos(theta), 0],
                           [0, 0, 0, 1]]), P)
    return Pl


def rotacaoY(theta, P=[], *args):
    Pl = np.dot(np.matrix([[math.cos(theta), 0, math.sin(theta), 0],
                           [0, 1, 0, 0],
                           [(-1) * math.sin(theta), 0, math.cos(theta), 0],
                           [0, 0, 0, 1]]), P)
    return Pl


def rotacaoZ(theta, P=[], *args):
    Pl = np.dot(np.matrix([[math.cos(theta), (-1) * math.sin(theta), 0, 0],
                           [math.sin(theta), math.cos(theta), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]]), P)
    return Pl


# def calibra(X, Y, Z):
#     global dx, dy, dz, b
#
#     pos = UR3.readPos_Co()
#
#     if b != 1:
#         dx = pos[0] - Z
#         dy = pos[1] + X
#         dz = pos[2] + Y
#         print('dx: ', dx)
#         b = 1
#
#     dx2 = pos[0] - Z
#     dy2 = pos[1] + X
#     dz2 = pos[2] + Y
#     dx = (dx2 + dx) / 2
#     dy = (dy2 + dy) / 2
#     dz = (dz2 + dz) / 2
#
#     return

# funcao q efetua a mudanca de origem do sensor, para coincidir com a do robo
def muda_origem(X, Y, Z):
    global dx, dy, dz

    # print(a)
    # print('dx')
    # print(dx)

    Pl = np.array([[X, Y, Z, 1]])
    Pl = Pl.T

    theta = -90 * math.pi / 180
    Pl = rotacaoX(theta, Pl)

    theta = -90 * math.pi / 180
    Pl = rotacaoZ(theta, Pl)

    Pl = translacao(54.06937179565429, -309.3607355117798, 814.7731872558594, Pl)

    # pos = UR3.readPos_Co()
    #83.66604881286621, -312.1294315338135, 961.9167785644531
    # 60.10645980834961, -304.8945907592773, 975.7568420410156
    # 91.91182594299316, -313.6481683731079, 962.3895263671875
    # 81.24210147857666, -286.3017059326172, 819.1599914550782
    # 72.06937179565429, -309.3607355117798, 897.7731872558594
    # Pl = translacao(pos[0] - Z, pos[1] + X, pos[2] + Y, Pl)
    # print('\n calibra')
    # print (pos[0] - Z, pos[1] + X, pos[2] + Y)

    # Pl = translacao(dx ,dy, dz, Pl)

    Pl = Pl.T
    return [Pl[0, 0], Pl[0, 1], Pl[0, 2]]


