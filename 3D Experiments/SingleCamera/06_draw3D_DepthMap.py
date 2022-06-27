import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

from cam_config import *

# Choose the to be tested image
imbgr = cv2.imread("./Results/depth_map2.png")

# Change color image zone
imrgb = cv2.cvtColor(imbgr, cv2.COLOR_BGR2RGB)
imlab = cv2.cvtColor(imbgr, cv2.COLOR_BGR2LAB)

# Contour map ------------
plt.figure(2)
y = range(imlab.shape[0])
x = range(imlab.shape[1])
X, Y = np.meshgrid(x, y)
plt.contour(Y, X, imlab[:, :, 0], 50)
plt.show()

# Surface map - single color ------------
plt.figure(3)
ax = plt.axes(projection='3d')
y = range(imlab.shape[0])
x = range(imlab.shape[1])
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, imlab[:, :, 0])
plt.show()

# Surf with color gradient --------------
fig = plt.figure(figsize=(14, 9))
ax = plt.axes(projection='3d')
my_cmap = plt.get_cmap('hot')
z = imlab[:, :, 0]
surf = ax.plot_surface(Y, X, -imlab[:, :, 0], cmap=my_cmap, edgecolor='none')

fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
ax.set_title('Surface plot')
plt.show()
