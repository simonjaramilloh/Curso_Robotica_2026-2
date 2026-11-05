from roboticstoolbox import Bicycle, EKF, RandomPath, LandmarkMap, RangeBearingSensor
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Covarianzas estándar
V = np.diag([0.02, np.deg2rad(0.5)])**2  
W = np.diag([0.1, np.deg2rad(1.0)])**2 
P0 = np.diag([0.05, 0.05, np.deg2rad(0.5)])**2 

robot = Bicycle(covar=V, animation=None)
robot.control = RandomPath(workspace=10)

# VARIACIÓN 2: Entorno con muy pocos landmarks (solo 5)
mapa = LandmarkMap(5, workspace=10)

sensor = RangeBearingSensor(
    robot=robot,
    map=mapa,
    covar=W,
    angle=[-pi/2, pi/2],
    range=4
)

slam = EKF(robot=(robot, V), P0=P0, sensor=(sensor, W), map=None)
slam.run(T=40)

# Gráfica de Mapa y Trayectorias
plt.figure(figsize=(10,8))
mapa.plot()
robot.plot_xy(color='blue', label='Trayectoria real')
slam.plot_xy(color='red', label='Trayectoria estimada')
slam.plot_ellipse(filled=True, facecolor="g", alpha=0.3)
plt.title('Variación 2: SLAM en Entorno Escaso (5 Landmarks)')
plt.legend()
plt.grid(True)
plt.axis('equal')

# Gráfica de Incertidumbre
plt.figure(figsize=(8,6))
plt.plot(slam.get_t(), slam.get_Pnorm(), linewidth=2, color='orange')
plt.xlabel('Tiempo [s]')
plt.ylabel('Incertidumbre (Norma de P)')
plt.title('Crecimiento de incertidumbre por falta de referencias')
plt.grid(True)
plt.show()