import UR3
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import os.path


def lerArquvios(nome,path):

    vm = np.zeros((len(path),len(nome)))
    mm = np.zeros((len(path),len(nome),3))

    cont = 0
    cont2 = 0
    for paths in path:

        for nomes in nome:

            caminho = paths + '\\' + nomes + '.csv'
            df = pd.read_csv(caminho)

            Rvel = df['Gripper Speed']
            HandX = df['Hand X']
            HandY = df['Hand Y']
            HandZ = df['Hand Z']

            HandXm = np.mean(HandX)
            HandYm = np.mean(HandY)
            HandZm = np.mean(HandZ)
            # Euc = math.sqrt(((Xml - Xr) ** 2.0) + ((Yml - Yr) ** 2.0) + ((Zml - Zr) ** 2.0))

            mm[cont,cont2] = [HandXm,HandYm,HandZm]
            vm[cont,cont2] = np.mean(Rvel) * 100
            cont2+=1
        cont+=1
        cont2 = 0
    return vm,mm


def seperar(vm,diff):

    vm2 = np.zeros((diff, len(vm)/diff, len(vm[0])))
    cont3=0
    for cont in range(diff):
        for cont2 in range(len(vm)/diff):
            vm2[cont,cont2] = vm[cont3,:]
            cont3+=1


    return vm2

def dataFrameVelmedia(vm, name='velm', sheetname=['Centroid','Bisector','Lom','Som','Mom']):
    # name = 'Exel\\' + name + '.csv'

    colunas0 = ['Square Route','Round Route','Collision Route','3-Dimension Route']

    for cont in range(len(vm)):
        dataframe = pd.DataFrame(vm[cont], columns=colunas0)
        dataframe.index.name = 'Id amostra'

        if os.path.isfile('VelData\\' + name + '.xlsx'):
            print("O arquivo ja existe")
            with pd.ExcelWriter('VelData\\' + name + '.xlsx',
                                mode='a') as writer:
                dataframe.to_excel(writer, sheet_name=sheetname[cont])
        else:
            print("O arquivo ainda nao existe")
            dataframe.to_excel('VelData\\' + name + '.xlsx', sheet_name=sheetname[cont])
    #
    # dataframe = [dataframe0, dataframe1, dataframe2, dataframe3, dataframe4]
    # dataframe = pd.concat(dataframe, axis=1, sort=False, join='outer')
    # dataframe.index.name = 'Id amostra'

    # if os.path.isfile('Exel\\' + name + '.xlsx'):
    #     print("O arquivo ja existe")
    #     cont = 1
    #     name = name + str(cont)
    #     while os.path.isfile('Exel\\' + name + '.xlsx'):
    #         name = name[:-len(str(cont))]
    #         cont += 1
    #         name = name + str(cont)
    #     dataframe.to_csv()
    #     with pd.ExcelWriter('Exel\\' + name + '.xlsx',
    #                         mode='a') as writer:
    #         dataframe.to_Exel(writer, sheet_name=sheetname)
    # else:
    #     print("O arquivo ainda nao existe")
    #     dataframe.to_csv('Exel\\' + name + '.csv')
    return

def main():
    path = ["Exel\Centroid","Exel\Centroid1","Exel\Centroid2","Exel\Centroid3","Exel\Centroid4","Exel\Centroid5",
            "Exel\Centroid6","Exel\Centroid7","Exel\Centroid8","Exel\Centroid9","Exel\Bisector","Exel\Bisector1",
            "Exel\Bisector2","Exel\Bisector3","Exel\Bisector4","Exel\Bisector5","Exel\Bisector6","Exel\Bisector7",
            "Exel\Bisector8","Exel\Bisector9","Exel\LoM","Exel\LoM1","Exel\LoM2","Exel\LoM3","Exel\LoM4","Exel\LoM5",
            "Exel\LoM6","Exel\LoM7","Exel\LoM8","Exel\LoM9","Exel\SoM","Exel\SoM1","Exel\SoM2","Exel\SoM3","Exel\SoM4",
            "Exel\SoM5","Exel\SoM6","Exel\SoM7","Exel\SoM8","Exel\SoM9","Exel\MoM","Exel\MoM1","Exel\MoM2","Exel\MoM3",
            "Exel\MoM4","Exel\MoM5","Exel\MoM6","Exel\MoM7","Exel\MoM8","Exel\MoM9"]

    nome = ["data","data1","data2","data3"]
    vm,mm = lerArquvios(nome,path)
    vm = seperar(vm,5)
    # print vm[0]
    dataFrameVelmedia(vm)
    # dataFrameVelmedia(vm)
    # for cont in range(len(path)):
    #     for cont2 in range(len(nome)):


if __name__ == "__main__":
    main()