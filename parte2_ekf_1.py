from roboticstoolbox import Bicycle, EKF, RandomPath
import numpy as np
import matplotlib.pyplot as plt

# VARIACIÓN 1: Ruido de odometría elevado (0.15 m y 3.0 grados)
V = np.diag([0.15, np.deg2rad(3.0)])**2

robot = Bicycle(covar=V, animation=None)
robot.control = RandomPath(workspace=10)

# Covarianza inicial normal
P0 = np.diag([0.05, 0.05, np.deg2rad(0.5)])**2

ekf = EKF(robot=(robot, V), P0=P0)
ekf.run(T=20)

# Gráfica de trayectorias
plt.figure(figsize=(8,6))
robot.plot_xy(color='blue', label='Trayectoria real')
ekf.plot_xy(color='red', label='Trayectoria estimada')
plt.title('Variación 1: EKF con Ruido de Odometría Severo (V alto)')
plt.legend()
plt.grid(True)

# Gráfica de incertidumbre
plt.figure(figsize=(8,6))
plt.plot(ekf.get_t(), ekf.get_Pnorm(), linewidth=2, color='orange')
plt.xlabel('Tiempo [s]')
plt.ylabel('Incertidumbre (Norma de P)')
plt.title('Crecimiento acelerado de incertidumbre')
plt.grid(True)
plt.show()