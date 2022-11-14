import pandas as pd
import os.path




def dataFrameCobot(Stamp, Robot_pos, Hand_pos, Robot_speed, Euclidean_dist, name, sheetname):
    # name = 'Exel\\' + name + '.csv'

    colunas0 = ['Time Stamp']
    colunas1 = ['Robot X', 'Robot Y', 'Robot Z']
    colunas2 = ['Hand X', 'Hand Y', 'Hand Z']
    colunas3 = ['Gripper Speed']
    colunas4 = ['Euclidean distance']
    dataframe0 = pd.DataFrame(Stamp[:], columns=colunas0)
    dataframe1 = pd.DataFrame(Robot_pos[:], columns=colunas1)
    dataframe2 = pd.DataFrame(Hand_pos[:], columns=colunas2)
    dataframe3 = pd.DataFrame(Robot_speed[:], columns=colunas3)
    dataframe4 = pd.DataFrame(Euclidean_dist[:], columns=colunas4)

    dataframe = [dataframe0, dataframe1, dataframe2, dataframe3, dataframe4]
    dataframe = pd.concat(dataframe, axis=1, sort=False, join='outer')
    dataframe.index.name = 'Id amostra'

    if os.path.isfile('Exel\\' + name + '.csv'):
        print("O arquivo ja existe")
        cont = 1
        name = name + str(cont)
        while os.path.isfile('Exel\\' + name + '.csv'):
            name = name[:-len(str(cont))]
            cont += 1
            name = name + str(cont)
        dataframe.to_csv('Exel\\' + name + '.csv')
        # with pd.ExcelWriter(name,
        #                     mode='a') as writer:
        #     dataframe.to_to_csv(writer, sheet_name=sheetname)
    else:
        print("O arquivo ainda nao existe")
        dataframe.to_csv('Exel\\' + name + '.csv')
    return
