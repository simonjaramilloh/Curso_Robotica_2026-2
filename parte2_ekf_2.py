from roboticstoolbox import Bicycle, EKF, RandomPath
import numpy as np
import matplotlib.pyplot as plt

# Ruido de odometría normal
V = np.diag([0.02, np.deg2rad(0.5)])**2

robot = Bicycle(covar=V, animation=None)
robot.control = RandomPath(workspace=10)

# VARIACIÓN 2: Alta incertidumbre inicial (1.0 m en ejes XY y 5.0 grados)
P0 = np.diag([1.0, 1.0, np.deg2rad(5.0)])**2

ekf = EKF(robot=(robot, V), P0=P0)

# Mayor tiempo de simulación
ekf.run(T=40)

# Gráfica de trayectorias
plt.figure(figsize=(8,6))
robot.plot_xy(color='blue', label='Trayectoria real')
ekf.plot_xy(color='red', label='Trayectoria estimada')
plt.title('Variación 2: EKF con Alta Incertidumbre Inicial (P0 alto)')
plt.legend()
plt.grid(True)

# Gráfica de incertidumbre
plt.figure(figsize=(8,6))
plt.plot(ekf.get_t(), ekf.get_Pnorm(), linewidth=2, color='green')
plt.xlabel('Tiempo [s]')
plt.ylabel('Incertidumbre (Norma de P)')
plt.title('Incertidumbre partiendo de un valor inicial alto')
plt.grid(True)
plt.show()