from roboticstoolbox import Bicycle
import numpy as np
import matplotlib.pyplot as plt

# Ruido moderado
V = np.diag([0.1, np.deg2rad(0.5)])**2
robot = Bicycle(covar=V)
robot_ideal = Bicycle(covar=np.zeros((2,2)))

x_real, y_real, x_ideal, y_ideal = [], [], [], []
qp_real = [0, 0, 0]
qp_ideal = [0, 0, 0]

for _ in range(200):
    # Cambio de control: Mayor velocidad (2.0) y giro hacia la derecha (-0.15)
    odo_real = robot.step((2.0, -0.15))
    qp_real = robot.f(qp_real, odo_real)
    
    odo_ideal = robot_ideal.step((2.0, -0.15))
    qp_ideal = robot.f(qp_ideal, odo_ideal)
    
    x_real.append(qp_real[0])
    y_real.append(qp_real[1])
    x_ideal.append(qp_ideal[0])
    y_ideal.append(qp_ideal[1])

plt.figure(figsize=(8,6))
plt.plot(x_ideal, y_ideal, label='Odometría ideal (sin ruido)', linewidth=1)
plt.plot(x_real, y_real, label='Odometría con ruido (Giro inverso)', linewidth=1)
plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.title('Variación 2: Trayectoria rápida con giro a la derecha')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()