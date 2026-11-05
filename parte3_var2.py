from roboticstoolbox import Bicycle, EKF, RandomPath, LandmarkMap, RangeBearingSensor
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# 1. Covarianza odometría (ruido del robot)
V = np.diag([0.02, np.deg2rad(0.5)])**2

# 2. Configurar Robot
robot = Bicycle(covar=V, animation=None)
robot.control = RandomPath(workspace=10)

# 3. Mapa de landmarks conocidos previamente
mapa = LandmarkMap(20, workspace=10)

# 4. Covarianza del sensor de rango (ruido del sensor)
W = np.diag([0.1, np.deg2rad(1)])**2

# 5. Sensor de rango y marcación (tipo LIDAR)
sensor = RangeBearingSensor(
    robot=robot,
    map=mapa,
    covar=W,
    angle=[-pi, pi],
    range=15
)

# 6. Covarianza inicial del robot
P0 = np.diag([0.05, 0.05, np.deg2rad(0.5)])**2

# 7. Crear el EKF
ekf = EKF(
    robot=(robot, V),
    P0=P0,
    map=mapa,
    sensor=(sensor, W)
)

# 8. Ejecutar simulación
ekf.run(T=40)

# 9. Graficar Trayectorias y Mapa
plt.figure(figsize=(10,8))
mapa.plot()
robot.plot_xy(color='blue', label='Trayectoria real')
ekf.plot_xy(color='red', label='Trayectoria estimada')
ekf.plot_ellipse(filled=True, facecolor="g", alpha=0.3)
plt.title('EKF con landmarks (Sensor de rango = 4m)')
plt.legend()
plt.grid(True)

# 10. Graficar Incertidumbre
plt.figure(figsize=(8,6))
plt.plot(ekf.get_t(), ekf.get_Pnorm(), linewidth=2)
plt.xlabel('Tiempo [s]')
plt.ylabel('Incertidumbre (Norma de P)')
plt.title('Incertidumbre con correcciones de Landmarks')
plt.grid(True)

plt.show()