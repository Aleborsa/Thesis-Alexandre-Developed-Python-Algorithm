import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

df = pd.read_csv("Exel/MoM/data1.csv")
# print (df['Time Stamp'])

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

ax = plt.axes(projection='3d')

# Data for a three-dimensional line
# zline = np.linspace(0, 10, 1000)
# xline = np.linspace(0, 10, 1000)
# yline = np.linspace(0, 10, 1000)
ax.plot3D(Rx, Ry, Rz, 'gray', alpha=0.1)
ax.plot3D(HandX, HandY, HandZ, 'gray', alpha=0.1)

# Data for three-dimensional scattered points
# zdata = 15 * np.random.random(100)
# xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
# ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(Rx, Ry, Rz, c=Rvel*100, cmap='jet',vmin=0,vmax=100, marker='s')
ax.scatter3D(HandXm, HandYm, HandZm, marker="D",color='r')
# ax.scatter3D(HandX, HandY, HandZ,c=Euc, cmap='seismic')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
plt.close()
# ax2 = plt.scatter( timestamp,Euc)
# ax2.scatter3D(Euc, , timestamp)
# font2 = {'style': 'oblique', 'color': 'black', 'size': 13}
# plt.scatter(HandXm, HandYm, marker="D",color='r')
# plt.scatter(Rx, Ry, c=Rvel*100, cmap='jet',vmin=0,vmax=100,marker='s')
# plt.xlabel('Distance in X (mm)', fontdict=font2)
# plt.ylabel('Distance in Y (mm)', fontdict=font2)
# plt.show()
# plt.close()
#
# plt.scatter(HandXm, HandZm, marker="D",color='r')
# plt.scatter(Rx, Rz, c=Rvel*100, cmap='jet',vmin=0,vmax=100,marker='s')
# plt.xlabel('Distance in X (mm)', fontdict=font2)
# plt.ylabel('Distance in Z (mm)', fontdict=font2)
# plt.show()
# plt.close()
#
# plt.scatter(HandYm, HandZm, marker="D",color='r')
# plt.scatter(Ry, Rz, c=Rvel*100, cmap='jet',vmin=0,vmax=100,marker='s')
# plt.xlabel('Distance in Y (mm)', fontdict=font2)
# plt.ylabel('Distance in Z (mm)', fontdict=font2)
# plt.show()
# plt.close()

plt.scatter(timestamp, Euc, c=Rvel*100, cmap='jet',vmin=0,vmax=100)
plt.show()
# ax2.set_xlabel('euc')
# ax2.set_ylabel('vel')
# ax2.set_zlabel('stamp')

