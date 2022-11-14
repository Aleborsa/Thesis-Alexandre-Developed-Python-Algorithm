import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math


def remove0(mat, mat2, size):
    n = 0
    for XYZ in mat:
        if XYZ.any() != 0:
            n += 1

    SEM0 = np.zeros([n, size])
    vel0 = np.zeros([n, 1])
    n = 0
    cont = 0
    for XYZ in mat:
        if XYZ.any() != 0:
            SEM0[n] = XYZ
            vel0[n] = mat2[cont]
            n += 1
        cont += 1
    return SEM0, vel0

def Dados2D(nome,path):
    i = 0
    for nomes in nome:

        pathf = path + '\\' + nomes + ".csv"
        df = pd.read_csv(pathf)

        timestamp = df['Time Stamp']
        Rx = df['Robot X']
        Ry = df['Robot Y']
        Rz = df['Robot Z']
        HandX = df['Hand X']
        HandY = df['Hand Y']
        HandZ = df['Hand Z']
        Rvel = df['Gripper Speed']
        Euc = df['Euclidean distance']

        tam = len(Rx)
        Desce = np.zeros([tam, 3])
        Sobe = np.zeros([tam, 3])
        Esquerda = np.zeros([tam, 3])
        Direita = np.zeros([tam, 3])
        velSobe = np.zeros(tam)
        velDesce = np.zeros(tam)
        velEsquerda = np.zeros(tam)
        velDireita = np.zeros(tam)

        cont = 0
        Xan = 0
        for X in Rx:

            if cont == 0:
                Xan = X
                Yan = Ry[cont]

            # Erro = (1 / 100) * X
            Erro = 1
            if (X + Erro) >= Xan >= (X - Erro):
                # print 'X mantei igual'

                Erro2 = 1
                if (Ry[cont] + Erro2) >= Yan >= (Ry[cont] - Erro2):
                    print 'Y mantei igual'
                elif (Ry[cont] - Yan < 0):
                    Esquerda[cont] = [X, Ry[cont], Rz[cont]]
                    velEsquerda[cont] = Rvel[cont]
                elif (Ry[cont] - Yan > 0):
                    Direita[cont] = [X, Ry[cont], Rz[cont]]
                    velDireita[cont] = Rvel[cont]

            elif (X - Xan < 0):
                Sobe[cont] = [X, Ry[cont], Rz[cont]]
                velSobe[cont] = Rvel[cont]
            elif (X - Xan > 0):
                Desce[cont] = [X, Ry[cont], Rz[cont]]
                velDesce[cont] = Rvel[cont]
            Xan = X
            Yan = Ry[cont]
            cont += 1

        Desce, velDesce = remove0(Desce, velDesce, 3)
        Sobe, velSobe = remove0(Sobe, velSobe, 3)
        Esquerda, velEsquerda = remove0(Esquerda, velEsquerda, 3)
        Direita, velDireita = remove0(Direita, velDireita, 3)

        HandXm = np.mean(HandX)
        HandYm = np.mean(HandY)
        HandZm = np.mean(HandZ)

        fig = plt.figure(figsize=(9, 8))



        plt.scatter(Rx[0], Ry[0], s=40, marker="s", color='black',label="Start Point")  # First point of the route
        plt.scatter(Sobe[:, 0], Sobe[:, 1], c=velSobe[:, 0] * 100, cmap='jet', vmin=0, vmax=100, marker="<")  #
        plt.scatter(Desce[:, 0], Desce[:, 1], c=velDesce[:, 0] * 100, cmap='jet', vmin=0, vmax=100, marker=">")
        plt.scatter(Esquerda[:, 0], Esquerda[:, 1], c=velEsquerda[:, 0] * 100, cmap='jet', vmin=0, vmax=100, marker="v")
        plt.scatter(Direita[:, 0], Direita[:, 1], c=velDireita[:, 0] * 100, cmap='jet', vmin=0, vmax=100, marker="^")
        plt.colorbar(ticks=range(0, 101, 5), label='Velocity (%)')

        plt.scatter(HandXm, HandYm, s=100, marker="D", color='r',label="Hand Position")
        plt.scatter(0, 0, s=100, marker="D", color='black',label="Origin (Cobot's Base)")

        minx = math.ceil(min(Rx) / 50) * 50
        maxx = math.ceil(max(Rx) / 50) * 50
        if minx > 0:
            minx = 0

        major_ticks_top = np.arange(minx, maxx, 1)
        step = major_ticks_top[1] - major_ticks_top[0]

        cont = 1
        while step % 10 != 0 or len(major_ticks_top) > 10:
            cont += 1
            major_ticks_top = np.arange(minx, maxx, cont)
            step = major_ticks_top[1] - major_ticks_top[0]

        ticksx = np.zeros(len(major_ticks_top) + 4)
        ticksx[2:len(major_ticks_top) + 2] = major_ticks_top
        ticksx[1] = (ticksx[2] - ticksx[3]) + ticksx[2]
        ticksx[0] = (ticksx[2] - ticksx[3]) + ticksx[1]
        ticksx[len(major_ticks_top) + 2] = -(ticksx[2] - ticksx[3]) + ticksx[len(major_ticks_top) + 1]
        ticksx[len(major_ticks_top) + 3] = -(ticksx[2] - ticksx[3]) + ticksx[len(major_ticks_top) + 2]

        miny = math.ceil(min(Ry) / 50) * 50
        maxy = math.ceil(max(Ry) / 50) * 50
        if miny > 0:
            miny = 0

        if miny > HandYm:
            miny = math.floor(HandYm / 50) * 50

        major_ticks_top = np.arange(miny, maxy, 1)
        step = major_ticks_top[1] - major_ticks_top[0]
        cont = 1
        while step % 10 != 0 or len(major_ticks_top) > 20:
            cont += 1
            major_ticks_top = np.arange(miny, maxy, cont)
            step = major_ticks_top[1] - major_ticks_top[0]

        ticksy = np.zeros(len(major_ticks_top) + 4)
        ticksy[2:len(major_ticks_top) + 2] = major_ticks_top
        ticksy[1] = (ticksy[2] - ticksy[3]) + ticksy[2]
        ticksy[0] = (ticksy[2] - ticksy[3]) + ticksy[1]
        ticksy[len(major_ticks_top) + 2] = -(ticksy[2] - ticksy[3]) + ticksy[len(major_ticks_top) + 1]
        ticksy[len(major_ticks_top) + 3] = -(ticksy[2] - ticksy[3]) + ticksy[len(major_ticks_top) + 2]

        plt.xticks(ticksx)
        plt.yticks(ticksy)
        plt.grid(visible=True, linestyle='-.', linewidth=0.4)

        font1 = {'color': 'black', 'size': 20}
        font2 = {'style': 'oblique', 'color': 'black', 'size': 13}

        plt.title('Robot Trajectory with Speed Data in XY Plane', fontdict=font1, weight='bold', y=1.05)
        plt.xlabel('Distance in X (mm)', fontdict=font2)
        plt.ylabel('Distance in Y (mm)', fontdict=font2)
        if i == 1:
            plt.legend(loc=4)
        else:
            plt.legend(loc=3)
        plt.plot(Rx, Ry, 'gray', alpha=0.1)  # gray line connecting each data point
        plt.savefig(path + '\\' + nomes + '_2D' + '.png',bbox_inches = 'tight', transparent = True)

        # plt.show()
        i+=1
        plt.close('all')

        # fig2 = plt.figure(figsize=(9, 8))
        #
        # ax = plt.axes(projection='3d')
        #
        # ax.plot3D(Rx, Ry, Rz, 'gray', alpha=0.1)
        # # ax.plot3D(HandX, HandY, HandZ, 'gray', alpha=0.1)
        #
        # ax.scatter3D(Rx[0], Ry[0], Rz[0], s=40, marker="s", color='black')
        # ax.scatter3D(Sobe[:, 0], Sobe[:, 1], Sobe[:, 2], c=velSobe[:, 0] * 100, cmap='jet', vmin=0, vmax=100,
        #              marker="^")
        # ax.scatter3D(Desce[:, 0], Desce[:, 1], Desce[:, 2], c=velDesce[:, 0] * 100, cmap='jet', vmin=0, vmax=100,
        #              marker="v")
        # ax.scatter3D(Esquerda[:, 0], Esquerda[:, 1], Esquerda[:, 2], c=velEsquerda[:, 0] * 100, cmap='jet', vmin=0,
        #              vmax=100, marker="<")
        # ma = ax.scatter3D(Direita[:, 0], Direita[:, 1], Direita[:, 2], c=velDireita[:, 0] * 100, cmap='jet', vmin=0,
        #                   vmax=100, marker=">")
        #
        # ax.scatter3D(HandXm, HandYm, HandZm, s=100, marker="D", color='r')
        # ax.scatter3D(0, 0, 0, s=50, marker="D", color='black')
        #
        # font1 = {'color': 'black', 'size': 20}
        # font2 = {'style': 'oblique', 'color': 'black', 'size': 13}
        #
        # ax.set_title('Robot Trajectory with Speed Data', fontdict=font1, weight='bold', y=1.05)
        # ax.set_xlabel('Distance in X (mm)', fontdict=font2)
        # ax.set_ylabel('Distance in Y (mm)', fontdict=font2)
        # ax.set_zlabel('Distance in Z (mm)', fontdict=font2)
        #
        # # ax.set_zlim3d(0, 100)
        # # ax.view_init(30, 325)
        # plt.colorbar(mappable=ma, ticks=range(0, 101, 5), label='Velocity (%)')
        # ax.view_init(35, -20)
        # plt.savefig(path + '\\' + nomes + '_3D' + '.png',bbox_inches = 'tight', transparent = True)
        # plt.show()
        # plt.close('all')

        # plt.scatter(timestamp, Euc, c=Rvel, cmap='viridis',vmin=0,vmax=1)
        # plt.grid(visible=True, linestyle='-.', linewidth=0.4)
        # plt.show()

def Dados3D(nome,path):
    for nomes in nome:

        pathf = path + "\\" + nomes + ".csv"
        df = pd.read_csv(pathf)

        timestamp = df['Time Stamp']
        Rx = df['Robot X']
        Ry = df['Robot Y']
        Rz = df['Robot Z']
        HandX = df['Hand X']
        HandY = df['Hand Y']
        HandZ = df['Hand Z']
        Rvel = df['Gripper Speed']
        Euc = df['Euclidean distance']


        HandXm = np.mean(HandX)
        HandYm = np.mean(HandY)
        HandZm = np.mean(HandZ)

        font1 = {'color': 'black', 'size': 20}
        font2 = {'style': 'oblique', 'color': 'black', 'size': 13}

        fig = plt.figure(figsize=(9, 8))

        ax = plt.axes(projection='3d')

        ax.plot3D(Rx, Ry, Rz, 'gray', alpha=0.1)

        list1 = ax.scatter3D(Rx[0], Ry[0], Rz[0], s=40, marker="s", color='black',label="Start Point")
        ma = ax.scatter3D(Rx[1:], Ry[1:], Rz[1:], c=Rvel[1:]*100, cmap='jet', vmin=0, vmax=100, marker='s')

        list2 = ax.scatter3D(HandXm, HandYm, HandZm, s=100, marker="D", color='r',label="Hand Position")
        list3 = ax.scatter3D(0, 0, 0, s=50, marker="D", color='black',label="Origin (Cobot's Base)")

        font1 = {'color': 'black', 'size': 20}
        font2 = {'style': 'oblique', 'color': 'black', 'size': 13}

        ax.set_title('Robot Trajectory with Speed Data', fontdict=font1, weight='bold', y=1.05)
        ax.set_xlabel('Distance in X (mm)', fontdict=font2)
        ax.set_ylabel('Distance in Y (mm)', fontdict=font2)
        ax.set_zlabel('Distance in Z (mm)', fontdict=font2)

        # ax.set_zlim3d(0, 100)
        ax.view_init(30, -20)
        plt.colorbar(mappable=ma, ticks=range(0, 101, 5),label='Velocity (%)')
        plt.legend(loc=2, handles=[list1, list2,list3],bbox_to_anchor=(-0.1, 0.8, 0.1, 0.15))
        plt.savefig(path + '\\' + nomes + '_3D' + '.png', bbox_inches = 'tight', transparent = True)
        # plt.show()
        plt.close('all')

        # fig2 = plt.figure(figsize=(9, 8))
        #
        # ax2 = plt.axes(projection='3d')
        # ax2.plot3D(Rx, Ry, Rz, 'black', alpha=1)
        # ax2.scatter3D(0, 0, 0, color = 'black',marker="D", alpha=1)
        # ax2.scatter3D(HandXm, HandYm, HandZm, s=100, marker="D", color='r')
        #
        # ax2.set_title('Robot Trajectory', fontdict=font1, weight='bold', y=1.05)
        # ax2.set_xlabel('Distance in X (mm)', fontdict=font2)
        # ax2.set_ylabel('Distance in Y (mm)', fontdict=font2)
        # ax2.set_zlabel('Distance in Z (mm)', fontdict=font2)
        #
        # ax2.view_init(30, -20)
        # plt.legend(loc=1, bbox_to_anchor=(0.6, 0.3, 0.5, 0.7))
        # plt.savefig(path + '\\' + nomes + '_route_3D' + '.png', bbox_inches = 'tight', transparent = True)
        #
        # plt.show()
        # plt.close('all')

        # plt.scatter(timestamp, Euc, c=Rvel, cmap='viridis',vmin=0,vmax=1)
        # plt.grid(visible=True, linestyle='-.', linewidth=0.4)
        # plt.show()

def velMedia(data,path):
    cont = 0
    vm = np.zeros(len(data))
    for nomes in data:

        pathf = path + "\\" + nomes + ".csv"
        df = pd.read_csv(pathf)

        Rvel = df['Gripper Speed']

        vm[cont] = np.mean(Rvel)
        cont+=1
    return vm


def Rotas(nome,path):
    rotas = ["Square","Round","Collision","3-Dimensional"]
    cont = 0
    for nomes in nome:

        pathf = path + '\\' + nomes + ".csv"
        df = pd.read_csv(pathf)

        Rx = df['Robot X']
        Ry = df['Robot Y']
        Rz = df['Robot Z']
        HandX = df['Hand X']
        HandY = df['Hand Y']
        HandZ = df['Hand Z']

        HandXm = np.mean(HandX)
        HandYm = np.mean(HandY)
        HandZm = np.mean(HandZ)

        font1 = {'color': 'black', 'size': 20}
        font2 = {'style': 'oblique', 'color': 'black', 'size': 13}

        fig2 = plt.figure(figsize=(7, 6))

        ax = plt.axes(projection='3d')

        ax.plot3D(Rx, Ry, Rz, 'black', alpha=1,label="Gripper's Trajectory")
        # ax.plot3D(HandX, HandY, HandZ, 'gray', alpha=0.1)

        ax.scatter3D(Rx[0], Ry[0], Rz[0], s=40, marker="s", color='black',label="Start Point")
        ax.scatter3D(HandXm, HandYm, HandZm, s=100, marker="D", color='r',label="Hand Position")
        ax.scatter3D(0, 0, 0, s=50, marker="D", color='black',label="Origin (Cobot's Base)")

        font1 = {'color': 'black', 'size': 20}
        font2 = {'style': 'oblique', 'color': 'black', 'size': 13}

        ax.set_title('Gripper\'s ' + rotas[cont] + ' Trajectory', fontdict=font1, weight='bold', y=1.08)
        ax.set_xlabel('Distance in X (mm)', fontdict=font2)
        ax.set_ylabel('Distance in Y (mm)', fontdict=font2)
        ax.set_zlabel('Distance in Z (mm)', fontdict=font2)

        # ax.set_zlim3d(0, 100)
        # ax.view_init(30, 325)
        ax.view_init(45, -25)
        plt.legend(loc=1,bbox_to_anchor=(0.6, 0.3, 0.5, 0.7))
        plt.savefig(rotas[cont] + '.png',bbox_inches = 'tight', transparent = True)
        # plt.show()
        plt.close('all')

        cont+=1


        # plt.scatter(timestamp, Euc, c=Rvel, cmap='viridis',vmin=0,vmax=1)
        # plt.grid(visible=True, linestyle='-.', linewidth=0.4)
        # plt.show()
    return

def NumberofLaps(nome,path):
    for nomes in nome:

        pathf = path + "\\" + nomes + ".csv"
        df = pd.read_csv(pathf)

        timestamp = df['Time Stamp']
        Rx = df['Robot X']
        Ry = df['Robot Y']
        Rz = df['Robot Z']
        Rvel = df['Gripper Speed']
        Euc = df['Euclidean distance']

        plt.scatter(timestamp, Euc, c=Rvel, cmap='viridis',vmin=0,vmax=1)
        # plt.grid(visible=True, linestyle='-.', linewidth=0.4)
        plt.show()

    return

def NumberofLaps2(nome,path):


    pathf = path + "\\" + nome + ".csv"
    df = pd.read_csv(pathf)

    Rx = df['Robot X']
    Ry = df['Robot Y']
    Rz = df['Robot Z']
    timestamp = df['Time Stamp']
    Rvel = df['Gripper Speed']
    Euc = df['Euclidean distance']

    Errx =0.14
    Err = 0.05

    ErromeX = Rx[0]*(1-Errx)
    ErromaX = Rx[0]*(1+Errx)

    ErromeY = Ry[0]*(1-Err)
    ErromaY = Ry[0]*(1+Err)

    ErromeZ = Rz[0]*(1-Err)
    ErromaZ = Rz[0]*(1+Err)

    ErroEucme = Euc[0]*(1-Err)
    ErroEucma = Euc[0]*(1+Err)

    if abs(Rx[0])-abs(ErromeX) < 7:
        if Rx[0] < 0:
            ErromeX = Rx[0] + 7
            ErromaX = Rx[0] - 7
        elif Rx[0] > 0:
            ErromeX = Rx[0] - 7
            ErromaX = Rx[0] + 7

    # print ErroEucme, Euc[0], ErroEucma
    # print ErromeX, Rx[0], ErromaX
    # print ErromeY, Ry[0], ErromaY
    # print ErromeZ, Rz[0], ErromaZ
    # print Rx[0], Ry[0], Rz[0], '\n'


    cont2=0
    n_voltas = 0
    for cont in range(len(Rx)):

        if cont2 > 0:
            cont2 -= 1
        if cont != 0 and cont != 1 and cont != 2 and cont != 3 and cont != 4 and cont != 5:
            if ErromeX <= Rx[cont] <= ErromaX or ErromaX <= Rx[cont] <= ErromeX:
                if ErromeY <= Ry[cont] <= ErromaY or ErromaY <= Ry[cont] <= ErromeY:
                    if ErromeZ <= Rz[cont] <= ErromaZ or ErromaZ <= Rz[cont] <= ErromeZ:
                        if ErroEucme <= Euc[cont] <= ErroEucma:

                            if cont2 == 0:
                                n_voltas += 1
                                cont2 = 30
                            # print cont
                            # print ErromeX,Rx[cont],ErromaX
                            # print ErroEucme, Euc[cont], ErroEucma
                            # print Rx[cont], Ry[cont], Rz[cont], '\n'

    return n_voltas



def main():
    # path = ["Exel\MoM"]
    # nome = ["data1",'data']
    # print path[0] + ' ' + str(NumberofLaps2(nome[0], path[0]))

    # path = ["Exel\Centroid","Exel\Bisector","Exel\LoM","Exel\SoM","Exel\MoM",]
    # nome = ["data","data1","data2","data3"]
    # for cont in range(len(path)):
    #     for cont2 in range(len(nome)):
    #         print path[cont] + ' ' + str(NumberofLaps2(nome[cont2],path[cont]))
    #     print '\n'

    # print n_voltas("Exel\SoM", "data1")
    # path = ["Exel\Centroid"]
    # nome2 = ['data1']
    # # Dados3D(nome)
    # Dados2D(nome2,path[0])

    path = ["Exel\Centroid","Exel\Bisector","Exel\LoM","Exel\SoM","Exel\MoM"]
    nome = ["data","data1","data2"]
    nome2 = ["data3"]
    for cont in range(len(path)):

        Dados2D(nome,path[cont])
        Dados3D(nome2,path[cont])


    # path = ["Exel\Centroid","Exel\Bisector","Exel\LoM","Exel\SoM","Exel\MoM"]
    # nome = ["data","data1","data2","data3"]
    # for cont in range(len(path)):
    #     NumberofLaps(nome,path[cont])

    # path = ["Exel\Bisector"]
    # nome = ["data","data1","data2","data3"]
    # for cont in range(len(path)):
    #     Rotas(nome,path[cont])


    # path = ["Exel\Centroid","Exel\Bisector","Exel\LoM","Exel\SoM","Exel\MoM"]
    # nome = ["data","data1","data2","data3"]
    # for cont in range(len(path)):
    #     print path[cont] + ' ' + str(velMedia(nome,path[cont]))
    #     print '\n'


if __name__ == "__main__":
    main()




#
#

