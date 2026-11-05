from roboticstoolbox import Bicycle, EKF, RandomPath, LandmarkMap, RangeBearingSensor
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# 1. Covarianzas del sistema
V = np.diag([0.02, np.deg2rad(0.5)])**2  # Odometría
W = np.diag([0.1, np.deg2rad(1)])**2     # Sensor de rango
P0 = np.diag([0.05, 0.05, np.deg2rad(0.5)])**2 # Incertidumbre inicial

# 2. Configuración de Robot y Mapa (El mapa real existe, pero el robot no lo conoce)
robot = Bicycle(covar=V, animation=None)
robot.control = RandomPath(workspace=10)
mapa = LandmarkMap(20, workspace=10)

# 3. Sensor tipo LIDAR
sensor = RangeBearingSensor(
    robot=robot,
    map=mapa,
    covar=W,
    angle=[-pi/2, pi/2],
    range=4
)

# 4. EKF configurado para SLAM (map=None)
slam = EKF(
    robot=(robot, V),
    P0=P0,
    sensor=(sensor, W),
    map=None # <--- CLAVE: El robot no conoce el mapa
)

# 5. Ejecutar simulación
slam.run(T=40)

# 6. Graficar resultados - Mapa y Trayectorias
plt.figure(figsize=(10,8))
mapa.plot() # Dibuja el mapa real como referencia
robot.plot_xy(color='blue', label='Trayectoria real')
slam.plot_xy(color='red', label='Trayectoria estimada')
slam.plot_ellipse(filled=True, facecolor="g", alpha=0.3)
plt.title('SLAM usando EKF (Mapa Desconocido)')
plt.legend()
plt.grid(True)
plt.axis('equal')

# 7. Graficar Incertidumbre
plt.figure(figsize=(8,6))
plt.plot(slam.get_t(), slam.get_Pnorm(), linewidth=2, color='purple')
plt.xlabel('Tiempo [s]')
plt.ylabel('Incertidumbre (Norma de P)')
plt.title('Evolución de incertidumbre en SLAM')
plt.grid(True)

plt.show()